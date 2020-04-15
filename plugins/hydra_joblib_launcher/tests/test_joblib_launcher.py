# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys

import pytest  # type: ignore
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root

from hydra_plugins.hydra_joblib_launcher.joblib_launcher import JoblibLauncher

chdir_plugin_root()


win_msg = "Windows is unsupported, due to stability issues with JobLib"


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)  # type: ignore
def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert JoblibLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@pytest.mark.parametrize("launcher_name, overrides", [("joblib", [])])
class TestJoblibLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    """

    pass


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
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


def test_example_app(sweep_runner: TSweepRunner) -> None:
    with sweep_runner(
        calling_file="example/my_app.py",
        calling_module=None,
        task_function=None,
        config_path=None,
        config_name="config",
        overrides=["task=1,2,3,4"],
    ) as sweep:
        overrides = {("task=1",), ("task=2",), ("task=3",), ("task=4",)}

        assert sweep.returns is not None and len(sweep.returns[0]) == 4
        for ret in sweep.returns[0]:
            assert tuple(ret.overrides) in overrides
