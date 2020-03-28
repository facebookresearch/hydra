# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Type

import pytest

from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.plugin import Plugin
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.utils import get_class

# This only test core plugins.
# Individual plugins are responsible to test that they are discoverable.
launchers = ["hydra._internal.core_plugins.basic_launcher.BasicLauncher"]
sweepers = ["hydra._internal.core_plugins.basic_sweeper.BasicSweeper"]
search_path_plugins: List[str] = []


@pytest.mark.parametrize(  # type: ignore
    "plugin_type, expected",
    [
        (Launcher, launchers),
        (Sweeper, sweepers),
        (SearchPathPlugin, search_path_plugins),
        (Plugin, launchers + sweepers + search_path_plugins),
    ],
)
def test_discover(plugin_type: Type[Plugin], expected: List[str]) -> None:
    plugins = Plugins.instance().discover(plugin_type)
    expected_classes = [get_class(c) for c in expected]
    for ex in expected_classes:
        assert ex in plugins
