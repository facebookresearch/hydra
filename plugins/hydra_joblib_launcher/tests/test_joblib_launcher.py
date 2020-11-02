# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import pytest
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root

from hydra_plugins.hydra_joblib_launcher.joblib_launcher import JoblibLauncher

chdir_plugin_root()


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert JoblibLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@pytest.mark.parametrize("launcher_name, overrides", [("joblib", [])])
class TestJoblibLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    """

    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        # joblib with process-based backend (default)
        (
            {
                "defaults": [
                    {"hydra/launcher": "joblib"},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ]
            },
            ["-m"],
        )
    ],
)
class TestJoblibLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass


def test_example_app(hydra_sweep_runner: TSweepRunner, tmpdir: Any) -> None:
    with hydra_sweep_runner(
        calling_file="example/my_app.py",
        calling_module=None,
        task_function=None,
        config_path=None,
        config_name="config",
        overrides=["task=1,2,3,4", f"hydra.sweep.dir={tmpdir}"],
    ) as sweep:
        overrides = {("task=1",), ("task=2",), ("task=3",), ("task=4",)}

        assert sweep.returns is not None and len(sweep.returns[0]) == 4
        for ret in sweep.returns[0]:
            assert tuple(ret.overrides) in overrides


@pytest.mark.parametrize(  # type: ignore
    "overrides",
    [
        "hydra.launcher.batch_size=1",
        "hydra.launcher.max_nbytes=10000",
        "hydra.launcher.max_nbytes=1M",
        "hydra.launcher.pre_dispatch=all",
        "hydra.launcher.pre_dispatch=10",
        "hydra.launcher.pre_dispatch=3*n_jobs",
    ],
)
def test_example_app_launcher_overrides(
    hydra_sweep_runner: TSweepRunner, overrides: str
) -> None:
    with hydra_sweep_runner(
        calling_file="example/my_app.py",
        calling_module=None,
        task_function=None,
        config_path=None,
        config_name="config",
        overrides=[overrides],
    ) as sweep:
        assert sweep.returns is not None and len(sweep.returns[0]) == 1
