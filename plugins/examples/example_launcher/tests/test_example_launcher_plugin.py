# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import pytest

from hydra.plugins import Launcher
from hydra._internal.plugins import Plugins
from hydra.test_utils.launcher_common_tests import LauncherTestSuite
from hydra_plugins.example_launcher import ExampleLauncher

# This has to be included here for the LauncherTestSuite to work.
# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401


def test_discovery():
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    :return:
    """
    assert ExampleLauncher.__name__ in [x.__name__ for x in Plugins.discover(Launcher)]


@pytest.mark.parametrize("launcher_name, overrides", [("example", [])])
class TestExampleLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    Note that hydra/launcher/example.yaml should be provided by this launcher.
    """

    pass
