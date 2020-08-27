# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from pathlib import Path
from typing import Type

import pytest
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_plugin_root

from hydra_plugins.hydra_submitit_launcher import submitit_launcher

chdir_plugin_root()


@pytest.mark.parametrize(  # type: ignore
    "cls", [submitit_launcher.LocalLauncher, submitit_launcher.SlurmLauncher]
)
def test_discovery(cls: Type[Launcher]) -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert cls.__name__ in [x.__name__ for x in Plugins.instance().discover(Launcher)]


@pytest.mark.parametrize(
    "launcher_name, overrides", [("submitit_local", ["hydra.launcher.timeout_min=2"])]
)
class TestSubmititLauncher(LauncherTestSuite):
    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        (
            {},
            [
                "-m",
                "hydra/hydra_logging=disabled",
                "hydra/job_logging=disabled",
                "hydra/launcher=submitit_local",
                "hydra.launcher.gpus_per_node=0",
                "hydra.launcher.timeout_min=1",
            ],
        ),
    ],
)
class TestSubmititLauncherIntegration(IntegrationTestSuite):
    pass


def test_example(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "example/my_app.py",
        "-m",
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra/launcher=submitit_local",
    ]
    subprocess.check_call(cmd)
