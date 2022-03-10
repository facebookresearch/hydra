# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.plugins import Plugins
from hydra.plugins.plugin import Plugin

from example_registered_plugin import ExampleRegisteredPlugin, register_example_plugin


def test_discovery() -> None:
    # Tests that this plugin can be discovered after Plugins.register is called

    plugin_name = ExampleRegisteredPlugin.__name__

    assert plugin_name not in [x.__name__ for x in Plugins.instance().discover(Plugin)]

    register_example_plugin()

    assert plugin_name in [x.__name__ for x in Plugins.instance().discover(Plugin)]


def test_example_plugin() -> None:
    a = ExampleRegisteredPlugin(10)
    assert a.add(20) == 30
