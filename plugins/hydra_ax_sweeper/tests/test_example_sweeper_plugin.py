# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra_plugins.hydra_ax_sweeper import AxSweeper


def test_discovery() -> None:
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert AxSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]
