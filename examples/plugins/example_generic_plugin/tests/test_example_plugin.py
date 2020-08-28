# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.plugins import Plugins
from hydra.plugins.plugin import Plugin

from hydra_plugins.example_generic_plugin.example_plugin import ExamplePlugin


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking at all Plugins
    assert ExamplePlugin.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Plugin)
    ]


def test_example_plugin() -> None:
    a = ExamplePlugin(10)
    assert a.add(20) == 30
