# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Type

import pytest

from hydra._internal.plugins import Plugins
from hydra.plugins import Launcher, Plugin, SearchPathPlugin, Sweeper
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
    plugins = Plugins.discover(plugin_type)
    expected_classes = [get_class(c) for c in sorted(expected)]
    for ex in expected_classes:
        assert ex in plugins
