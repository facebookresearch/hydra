# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
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
    launchers = Plugins.discover(Launcher)
    # discovered plugins are actually different class objects, compare by name
    assert SubmititLauncher.__name__ in [x.__name__ for x in launchers]


@pytest.mark.parametrize(
    "launcher_name, overrides", [("submitit", ["hydra.launcher.params.queue=local"])]
)
class TestSubmititLauncher(LauncherTestSuite):
    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags, plugin_module",
    [
        (
            {
                "defaults": [
                    {"hydra/launcher": None},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ],
                "hydra": {
                    "launcher": {
                        "class": "hydra_plugins.submitit.SubmititLauncher",
                        "params": {
                            "queue": "local",
                            "folder": "${hydra.sweep.dir}/.${hydra.launcher.params.queue}",
                            "queue_parameters": {
                                "local": {
                                    "gpus_per_node": 1,
                                    "tasks_per_node": 1,
                                    "timeout_min": 1,
                                }
                            },
                        },
                    }
                },
            },
            ["-m"],
            "hydra_plugins.submitit",
        )
    ],
)
class TestSubmititLauncherIntegration(IntegrationTestSuite):
    pass
