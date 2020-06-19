# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Type

import pytest  # type: ignore
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_plugin_root

from hydra_plugins.hydra_submitit_launcher import submitit_launcher

chdir_plugin_root()


@pytest.mark.parametrize(
    "cls",
    [submitit_launcher.LocalSubmititLauncher, submitit_launcher.SlurmSubmititLauncher],
)
def test_discovery(cls: Type[Launcher]) -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert cls.__name__ in [x.__name__ for x in Plugins.instance().discover(Launcher)]


@pytest.mark.parametrize(
    "launcher_name, overrides",
    [("submitit_local", ["hydra.launcher.params.timeout_min=2"])],
)
class TestSubmititLauncher(LauncherTestSuite):
    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        (
            {
                "defaults": [
                    {"hydra/launcher": "submitit_local"},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ],
                "hydra": {
                    "launcher": {"params": {"gpus_per_node": 0, "timeout_min": 1}},
                },
            },
            ["-m"],
        ),
    ],
)
class TestSubmititLauncherIntegration(IntegrationTestSuite):
    pass
