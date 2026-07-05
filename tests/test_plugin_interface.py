# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys
import types
from typing import List, Sequence, Type

from omegaconf import DictConfig, OmegaConf
from pytest import MonkeyPatch, mark, raises

from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.plugins import Plugins
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.plugins.plugin import Plugin
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext, TaskFunction
from hydra.utils import get_class

# This only test core plugins.
# Individual plugins are responsible to test that they are discoverable.
launchers = ["hydra._internal.core_plugins.basic_launcher.BasicLauncher"]
sweepers = ["hydra._internal.core_plugins.basic_sweeper.BasicSweeper"]
search_path_plugins: List[str] = []


class PluginWithNestedTarget(Launcher):
    def __init__(self, nested: DictConfig) -> None:
        self.nested = nested

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None: ...

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        raise NotImplementedError()


PluginWithNestedTarget.__module__ = "hydra._internal.core_plugins.test_plugin"


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


def test_register_plugin() -> None:
    class MyPlugin(SearchPathPlugin):
        def manipulate_search_path(self, search_path: ConfigSearchPath) -> None: ...

    Plugins.instance().register(MyPlugin)

    assert MyPlugin in Plugins.instance().discover(Plugin)
    assert MyPlugin in Plugins.instance().discover(SearchPathPlugin)
    assert MyPlugin not in Plugins.instance().discover(Launcher)


def test_register_bad_plugin() -> None:
    class NotAPlugin: ...

    with raises(ValueError, match="Not a valid Hydra Plugin"):
        Plugins.instance().register(NotAPlugin)  # type: ignore


def test_plugin_instantiation_is_not_recursive(monkeypatch: MonkeyPatch) -> None:
    classname = "hydra._internal.core_plugins.test_plugin.PluginWithNestedTarget"
    module = types.ModuleType("hydra._internal.core_plugins.test_plugin")
    setattr(module, "PluginWithNestedTarget", PluginWithNestedTarget)
    monkeypatch.setitem(sys.modules, module.__name__, module)
    monkeypatch.setitem(
        Plugins.instance().class_name_to_class, classname, PluginWithNestedTarget
    )

    plugin = Plugins.instance()._instantiate(
        OmegaConf.create(
            {
                "_target_": classname,
                "nested": {
                    "_target_": "tests.instantiate.AClass",
                    "a": 1,
                    "b": 2,
                    "c": 3,
                },
            }
        )
    )

    assert isinstance(plugin, PluginWithNestedTarget)
    assert isinstance(plugin.nested, DictConfig)
    assert plugin.nested._target_ == "tests.instantiate.AClass"
