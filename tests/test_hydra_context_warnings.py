# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from textwrap import dedent
from typing import Any, List, Sequence, Union
from unittest.mock import Mock

from omegaconf import DictConfig, OmegaConf
from pytest import mark, warns

from hydra import TaskFunction
from hydra._internal.callbacks import Callbacks
from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.utils import create_config_search_path
from hydra.core.config_loader import ConfigLoader
from hydra.core.plugins import Plugins
from hydra.core.utils import JobReturn, _get_callbacks_for_run_job
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import chdir_hydra_root
from hydra.types import HydraContext

chdir_hydra_root()


class IncompatibleSweeper(Sweeper):
    def __init__(self) -> None:
        pass

    def setup(  # type: ignore
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        pass

    def sweep(self, arguments: List[str]) -> Any:
        pass


class IncompatibleLauncher(Launcher):
    def __init__(self) -> None:
        pass

    def setup(  # type: ignore
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        pass

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        pass


@mark.parametrize(
    "plugin, config",
    [
        (IncompatibleLauncher(), OmegaConf.create({"hydra": {"launcher": {}}})),
        (IncompatibleSweeper(), OmegaConf.create({"hydra": {"sweeper": {}}})),
    ],
)
def test_setup_plugins(
    monkeypatch: Any, plugin: Union[Launcher, Sweeper], config: DictConfig
) -> None:
    task_function = Mock(spec=TaskFunction)
    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    hydra_context = HydraContext(config_loader=config_loader, callbacks=Callbacks())
    plugin_instance = Plugins.instance()
    monkeypatch.setattr(Plugins, "check_usage", lambda _: None)
    monkeypatch.setattr(plugin_instance, "_instantiate", lambda _: plugin)

    msg = dedent(
        """
        Plugin's setup() signature has changed in Hydra 1.1.
        Support for the old style will be removed in Hydra 1.2.
        For more info, check https://github.com/facebookresearch/hydra/pull/1581."""
    )
    with warns(expected_warning=UserWarning, match=re.escape(msg)):
        if isinstance(plugin, Launcher):
            Plugins.instance().instantiate_launcher(
                task_function=task_function,
                config=config,
                config_loader=config_loader,
                hydra_context=hydra_context,
            )
        else:
            Plugins.instance().instantiate_sweeper(
                hydra_context=hydra_context,
                task_function=task_function,
                config=config,
            )


def test_run_job() -> None:
    hydra_context = None
    msg = dedent(
        """
        run_job's signature has changed in Hydra 1.1. Please pass in hydra_context.
        Support for the old style will be removed in Hydra 1.2.
        For more info, check https://github.com/facebookresearch/hydra/pull/1581."""
    )
    with warns(expected_warning=UserWarning, match=msg):
        _get_callbacks_for_run_job(hydra_context)
