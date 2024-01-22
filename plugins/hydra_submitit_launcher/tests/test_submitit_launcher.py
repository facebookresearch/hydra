# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from typing import Type

from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_plugin_root, run_python_script
from pytest import mark

from hydra_plugins.hydra_submitit_launcher import submitit_launcher

chdir_plugin_root()


@mark.parametrize(
    "cls", [submitit_launcher.LocalLauncher, submitit_launcher.SlurmLauncher]
)
def test_discovery(cls: Type[Launcher]) -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert cls.__name__ in [x.__name__ for x in Plugins.instance().discover(Launcher)]


@mark.parametrize(
    "launcher_name, overrides", [("submitit_local", ["hydra.launcher.timeout_min=2"])]
)
class TestSubmititLauncher(LauncherTestSuite):
    pass


@mark.parametrize(
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
    run_python_script(
        [
            "example/my_app.py",
            "-m",
            f"hydra.sweep.dir={tmpdir}",
            "hydra/launcher=submitit_local",
        ],
        allow_warnings=True,
    )
