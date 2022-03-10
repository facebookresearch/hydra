# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.plugins import Plugins
from hydra.plugins.plugin import Plugin


class ExampleRegisteredPlugin(Plugin):
    def __init__(self, v: int) -> None:
        self.v = v

    def add(self, x: int) -> int:
        return self.v + x


def register_example_plugin() -> None:
    """The Hydra user should call this function before invoking @hydra.main"""
    Plugins.instance().register(ExampleRegisteredPlugin)
