# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any, Optional
from unittest.mock import Mock

from omegaconf import DictConfig
from pytest import mark, raises, warns

from hydra import TaskFunction
from hydra.core.config_loader import ConfigLoader
from hydra.core.plugins import Plugins
from hydra.core.utils import _get_callbacks_for_run_job
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import chdir_hydra_root
from hydra.types import HydraContext

chdir_hydra_root()

plugins = Plugins.instance()


@mark.parametrize(
    "config_loader, hydra_context, setup_method, expected",
    [
        (None, None, lambda foo, bar: None, AssertionError),
        (
            Mock(ConfigLoader),
            None,
            lambda config_loader, config, task_function: None,
            UserWarning(),
        ),
        (
            Mock(spec=ConfigLoader),
            Mock(spec=HydraContext),
            lambda hydra_context, config, task_function: None,
            None,
        ),
    ],
)
def test_setup_plugin(
    config_loader: Optional[ConfigLoader],
    hydra_context: Optional[HydraContext],
    setup_method: Any,
    expected: Any,
) -> None:
    plugin = Mock(spec=Sweeper)
    plugin.setup = setup_method
    config = Mock(spec=DictConfig)
    task_function = Mock(spec=TaskFunction)
    msg = (
        "\n"
        "\tPlugin's setup() signature has changed in Hydra 1.1.\n"
        "\tSupport for the old style will be removed in Hydra 1.2.\n"
    )
    if expected is None:
        plugins._setup_plugin(
            plugin, config, task_function, config_loader, hydra_context
        )
    elif isinstance(expected, UserWarning):
        with warns(expected_warning=UserWarning, match=re.escape(msg)):
            plugins._setup_plugin(
                plugin, task_function, config, config_loader, hydra_context
            )
    else:
        with raises(expected):
            plugins._setup_plugin(
                plugin, config, task_function, config_loader, hydra_context
            )


def test_run_job() -> None:
    hydra_context = None
    msg = (
        "\n"
        "\trun_job's signature has changed in Hydra 1.1.\n"
        "\tSupport for the old style will be removed in Hydra 1.2.\n"
    )
    with warns(expected_warning=UserWarning, match=msg):
        _get_callbacks_for_run_job(hydra_context)
