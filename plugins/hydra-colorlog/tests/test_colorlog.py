# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

# TODO

# from hydra._internal.plugins import Plugins
# from hydra_plugins.example_plugin import ExamplePlugin
#
#
# def test_discovery():
#     # This may seem weird, but it verifies that we can discover this Plugin via
#     # the plugins subsystem.
#     # The discover method takes a class and return all plugins that implements that class.
#     # Typically we would be discovering all plugins that implementing some common interface.
#     plugins = Plugins.discover(ExamplePlugin)
#     # discovered plugins are actually different class objects, compare by name
#     assert ExamplePlugin.__name__ in [x.__name__ for x in plugins]
#
#
# def test_example_plugin():
#     from hydra_plugins.example_plugin import ExamplePlugin
#
#     a = ExamplePlugin(10)
#     assert a.add(20) == 30
