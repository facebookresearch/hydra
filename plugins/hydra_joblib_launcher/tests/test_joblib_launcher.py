# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys

import pytest

from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)

# This has to be included here for the LauncherTestSuite to work.
# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401
from hydra_plugins.hydra_joblib_launcher import JoblibLauncher

windows_reason = (
    "Windows is unsupported, due to issues with Joblib (related Joblib issue: #964)"
)


@pytest.mark.skipif(sys.platform.startswith("win"), reason=windows_reason)
def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert JoblibLauncher.__name__ in [x.__name__ for x in Plugins.discover(Launcher)]


@pytest.mark.skipif(sys.platform.startswith("win"), reason=windows_reason)
@pytest.mark.parametrize("launcher_name, overrides", [("joblib", [])])
class TestJoblibLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    Note that hydra/launcher/joblib.yaml should be provided by this launcher.
    """

    pass


@pytest.mark.skipif(sys.platform.startswith("win"), reason=windows_reason)
@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags, plugin_module",
    [
        # joblib with process-based backend (default)
        (
            {
                "defaults": [
                    {"hydra/launcher": "joblib"},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ],
            },
            ["-m"],
            "hydra_plugins.joblib_launcher",
        ),
        # joblib with thread-based backend
        (
            {
                "defaults": [
                    {"hydra/launcher": "joblib"},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ],
                "hydra": {"launcher": {"params": {"joblib": {"prefer": "threads"}}}},
            },
            ["-m"],
            "hydra_plugins.joblib_launcher",
        ),
    ],
)
class TestJoblibLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass
