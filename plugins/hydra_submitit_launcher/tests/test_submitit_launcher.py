# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest  # type: ignore
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_plugin_root

from hydra_plugins.hydra_submitit_launcher.submitit_launcher import SubmititLauncher

chdir_plugin_root()


def test_discovery():
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert SubmititLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


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
