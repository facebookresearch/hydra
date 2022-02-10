# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, List, Type

from pytest import mark

from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.plugins import Plugins
from hydra.core.singleton import Singleton
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


@mark.parametrize(
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


def test_automatic_plugin_subclass_discovery(hydra_restore_singletons: Any) -> None:
    # hack to deinitialize the Plugins singleton:
    Singleton._instances.pop(Plugins, None)

    class MyPlugin(SearchPathPlugin):
        def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
            ...

    class MyPluginSubclass(MyPlugin):
        ...

    assert MyPlugin in Plugins.instance().discover(Plugin)
    assert MyPlugin in Plugins.instance().discover(SearchPathPlugin)
    assert MyPlugin not in Plugins.instance().discover(Launcher)
    assert MyPluginSubclass in Plugins.instance().discover(Plugin)
    assert MyPluginSubclass in Plugins.instance().discover(SearchPathPlugin)
    assert MyPluginSubclass not in Plugins.instance().discover(Launcher)
