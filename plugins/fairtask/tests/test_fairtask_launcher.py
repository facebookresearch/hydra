# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest
from hydra_plugins.fairtask.fairtask_launcher import FAIRTaskLauncher

from hydra._internal.plugins import Plugins
from hydra.plugins import Launcher
from hydra.test_utils.launcher_common_tests import LauncherTestSuite
from hydra.test_utils.test_utils import chdir_hydra_root

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401

chdir_hydra_root()


def test_discovery():
    launchers = Plugins.discover(Launcher)
    # discovered plugins are actually different class objects, compare by name
    assert FAIRTaskLauncher.__name__ in [x.__name__ for x in launchers]


@pytest.mark.parametrize(
    "launcher_name, overrides",
    [
        (
            "fairtask",
            [
                "hydra.launcher.params.queue=local",
                "hydra.launcher.params.no_workers=true",
            ],
        )
    ],
)
class TestFAIRTaskLauncher(LauncherTestSuite):
    pass
