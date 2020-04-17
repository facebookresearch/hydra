# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest  # type: ignore
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)

from hydra_plugins.example_launcher_plugin.example_launcher import ExampleLauncher


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert ExampleLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@pytest.mark.parametrize("launcher_name, overrides", [("example", [])])
class TestExampleLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    Note that hydra/launcher/example.yaml should be provided by this launcher.
    """

    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
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
                        "cls": "hydra_plugins.example_launcher_plugin.example_launcher.ExampleLauncher",
                        "params": {"foo": 10, "bar": "abcde"},
                    }
                },
            },
            ["-m"],
        )
    ],
)
class TestExampleLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass
