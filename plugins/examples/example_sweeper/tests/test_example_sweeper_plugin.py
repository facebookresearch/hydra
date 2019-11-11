# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra_plugins.example_sweeper import ExampleSweeper

from hydra._internal.plugins import Plugins
from hydra.plugins import Sweeper


def test_discovery():
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert ExampleSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


# TODO: create tests for ExampleSweeper
