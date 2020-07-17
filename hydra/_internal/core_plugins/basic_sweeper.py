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
"""
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence

from omegaconf import MISSING, DictConfig, OmegaConf

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_store import ConfigStore
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import ObjectConf, TaskFunction


@dataclass
class BasicSweeperConf(ObjectConf):
    target: str = MISSING

    @dataclass
    class Params:
        max_batch_size: Optional[int] = None

    params: Params = Params()


ConfigStore.instance().store(
    group="hydra/sweeper", name="basic", node=BasicSweeperConf, provider="hydra",
)


class BasicSweeper(Sweeper):
    """
    Basic sweeper
    """

    def __init__(self, max_batch_size: Optional[int]) -> None:
        """
        Instantiates
        """
        super(BasicSweeper, self).__init__()
        self.overrides: Optional[Sequence[Sequence[Sequence[str]]]] = None
        self.batch_index = 0
        self.max_batch_size = max_batch_size

        self.config_loader: Optional[ConfigLoader] = None
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        from hydra.core.plugins import Plugins

        self.config_loader = config_loader
        self.config = config

        self.launcher = Plugins.instance().instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

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
        arguments: List[str], max_batch_size: Optional[int]
    ) -> List[List[List[str]]]:
        parser = OverridesParser()
        parsed = parser.parse_overrides(arguments)

        lists = []
        for override in parsed:
            if override.is_sweep_override():
                sweep_choices = override.choices_as_strings()
                assert isinstance(sweep_choices, list)
                key = override.get_key_element()
                sweep = [f"{key}={val}" for val in sweep_choices]
                lists.append(sweep)
            else:
                key = override.get_key_element()
                value = override.get_value_element()
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

    def sweep(self, arguments: List[str]) -> Any:
        assert self.config is not None
        assert self.launcher is not None
        self.overrides = self.split_arguments(arguments, self.max_batch_size)
        returns: List[Sequence[JobReturn]] = []

        # Save sweep run config in top level sweep working directory
        sweep_dir = Path(self.config.hydra.sweep.dir)
        sweep_dir.mkdir(parents=True, exist_ok=True)
        OmegaConf.save(self.config, sweep_dir / "multirun.yaml")

        initial_job_idx = 0
        while not self.is_done():
            batch = self.get_job_batch()
            self.validate_batch_is_legal(batch)
            results = self.launcher.launch(batch, initial_job_idx=initial_job_idx)
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
