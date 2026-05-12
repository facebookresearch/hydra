# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

"""
Basic sweeper can generate cartesian products of multiple input commands, each with a
comma separated list of values.
for example, for:
python foo.py a=1,2,3 b=10,20
Basic Sweeper would generate 6 jobs:
1,10
1,20
2,10
2,20
3,10
3,20

The Basic Sweeper also support, the following is equivalent to the above.
python foo.py a=range(1,4) b=10,20
"""
import itertools
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from omegaconf import DictConfig, OmegaConf
from omegaconf._utils import is_structured_config

from hydra.core.config_store import ConfigStore
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import Override, QuotedString
from hydra.core.utils import JobReturn
from hydra.errors import HydraException
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext, TaskFunction


@dataclass
class BasicSweeperConf:
    _target_: str = "hydra._internal.core_plugins.basic_sweeper.BasicSweeper"
    max_batch_size: Optional[int] = None
    params: Optional[Dict[str, str]] = None


ConfigStore.instance().store(
    group="hydra/sweeper", name="basic", node=BasicSweeperConf, provider="hydra"
)


log = logging.getLogger(__name__)


class BasicSweeper(Sweeper):
    """
    Basic sweeper
    """

    def __init__(
        self, max_batch_size: Optional[int], params: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Instantiates
        """
        super().__init__()

        if params is None:
            params = {}
        self.overrides: Optional[Sequence[Sequence[Sequence[str]]]] = None
        self.batch_index = 0
        self.max_batch_size = max_batch_size
        self.params = params

        self.hydra_context: Optional[HydraContext] = None
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        from hydra.core.plugins import Plugins

        self.hydra_context = hydra_context
        self.config = config

        self.launcher = Plugins.instance().instantiate_launcher(
            hydra_context=hydra_context,
            task_function=task_function,
            config=config,
        )

    @staticmethod
    def simplify_overrides(
        overrides: List[Override],
    ) -> List[Override]:
        # this would simplify the overrides by removing those that are overridden later
        # in the list.
        # e.g. a=1 and later a=10 would remove the first override.
        lists = []
        # NOTE: key -> index of last override with no dict value. (e.g. a=1,2,3)
        # any override for key before this would be skipped.
        last_primitive = {}
        last_dict = {}
        last_defaults: Dict[str, int] = {}

        is_defaults: Dict[int, bool] = {}
        is_primitive: Dict[int, bool] = {}
        has_dict: Dict[int, bool] = {}

        # check value should override earlier ones
        # TODO: handle extend_list
        def check_write_override(x: Any):
            return (
                isinstance(x, (str, int, float, bool, list, QuotedString)) or x is None
            )

        def check_has_dict(x: Any):
            return isinstance(x, dict) or is_structured_config(x)

        for i, override in enumerate(overrides):
            if override.config_loader is None:
                continue
            is_group = (
                len(override.config_loader.get_group_options(override.key_or_group)) > 0
            )

            key = override.get_key_element()
            _write = False
            _has_dict = False
            if override.is_sweep_override():
                if override.is_discrete_sweep():
                    _write = all(override.sweep_iterator(check_write_override))
                    _has_dict = any(override.sweep_iterator(check_has_dict))
            else:
                _write = check_write_override(override.value())
                _has_dict = check_has_dict(override.value())

            if _write:
                if is_group:
                    is_defaults[i] = True
                    if override.is_change():
                        last_defaults[key] = i
                else:
                    is_primitive[i] = True
                    last_primitive[key] = i
            if _has_dict:
                has_dict[i] = True
                last_dict[key] = i

        for i, override in enumerate(overrides):
            key = override.get_key_element()
            if is_primitive.get(i, False) and (
                last_primitive.get(key, -1) != i or last_dict.get(key, -1) > i
            ):
                continue
            if has_dict.get(i, False) and last_primitive.get(key, -1) > i:
                continue
            if is_defaults.get(i, False) and last_defaults.get(key, -1) > i:
                continue
            lists.append(override)

        return lists

    @staticmethod
    def split_overrides_to_chunks(
        lst: List[List[str]], n: Optional[int]
    ) -> Iterable[List[List[str]]]:
        if n is None or n == -1:
            n = len(lst)
        assert n > 0
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    @staticmethod
    def split_arguments(
        overrides: List[Override], max_batch_size: Optional[int]
    ) -> List[List[List[str]]]:
        lists = []
        overrides = BasicSweeper.simplify_overrides(overrides)
        for override in overrides:
            if override.is_sweep_override():
                if override.is_discrete_sweep():
                    key = override.get_key_element()
                    sweep = [f"{key}={val}" for val in override.sweep_string_iterator()]
                    lists.append(sweep)
                else:
                    assert override.value_type is not None
                    raise HydraException(
                        f"{BasicSweeper.__name__} does not support sweep type : {override.value_type.name}"
                    )
            else:
                key = override.get_key_element()
                value = override.get_value_element_as_str()
                lists.append([f"{key}={value}"])

        all_batches = [list(x) for x in itertools.product(*lists)]
        assert max_batch_size is None or max_batch_size > 0
        if max_batch_size is None:
            return [all_batches]
        else:
            chunks_iter = BasicSweeper.split_overrides_to_chunks(
                all_batches, max_batch_size
            )
            return [x for x in chunks_iter]

    def _parse_config(self) -> List[str]:
        params_conf = []
        for k, v in self.params.items():
            params_conf.append(f"{k}={v}")
        return params_conf

    def sweep(self, arguments: List[str]) -> Any:
        assert self.config is not None
        assert self.launcher is not None
        assert self.hydra_context is not None

        params_conf = self._parse_config()
        params_conf.extend(arguments)

        parser = OverridesParser.create(config_loader=self.hydra_context.config_loader)
        overrides = parser.parse_overrides(params_conf)

        self.overrides = self.split_arguments(overrides, self.max_batch_size)
        returns: List[Sequence[JobReturn]] = []

        # Save sweep run config in top level sweep working directory
        sweep_dir = Path(self.config.hydra.sweep.dir)
        sweep_dir.mkdir(parents=True, exist_ok=True)
        OmegaConf.save(self.config, sweep_dir / "multirun.yaml")

        initial_job_idx = 0
        while not self.is_done():
            batch = self.get_job_batch()
            tic = time.perf_counter()
            # Validate that jobs can be safely composed. This catches composition errors early.
            # This can be a bit slow for large jobs. can potentially allow disabling from the config.
            self.validate_batch_is_legal(batch)
            elapsed = time.perf_counter() - tic
            log.debug(
                f"Validated configs of {len(batch)} jobs in {elapsed:0.2f} seconds, {len(batch)/elapsed:.2f} / second)"
            )
            results = self.launcher.launch(batch, initial_job_idx=initial_job_idx)

            for r in results:
                # access the result to trigger an exception in case the job failed.
                _ = r.return_value

            initial_job_idx += len(batch)
            returns.append(results)

        return returns

    def get_job_batch(self) -> Sequence[Sequence[str]]:
        """
        :return: A list of lists of strings, each inner list is the overrides for a single job
        that should be executed.
        """
        assert self.overrides is not None
        self.batch_index += 1
        return self.overrides[self.batch_index - 1]

    def is_done(self) -> bool:
        assert self.overrides is not None
        return self.batch_index >= len(self.overrides)
