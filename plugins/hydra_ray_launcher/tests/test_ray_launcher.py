# # Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys

import pytest
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_plugin_root

from hydra_plugins.hydra_ray_launcher.ray_launcher import RayLauncher  # type: ignore

chdir_plugin_root()

win_msg = "Ray doesn't support Windows."


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)  # type: ignore
def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert RayLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@pytest.mark.parametrize("launcher_name, overrides", [("ray", [])])
class TestRayLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    """

    pass


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        (
            {},
            [
                "-m",
                "hydra/launcher=ray",
                "hydra/hydra_logging=hydra_debug",
                "hydra/job_logging=disabled",
            ],
        )
    ],
)
class TestRayLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass
