# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra._internal.plugins import Plugins
from hydra.plugins import Sweeper
from hydra_plugins.hydra_ax import AxSweeper
from hydra_plugins.hydra_ax.ax_sweeper import map_params_to_arg_list


def test_discovery():
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert AxSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


# TODO: create tests for ExampleSweeper


def test_map_params_to_arg_list():
    """Method to test the map_params_to_arg_list method"""
    params = {
        "x1": 0.1087956354022026,
        "x2": 0.506428062915802,
        "x3": 0.12900789082050323,
        "x4": 0.3486773371696472,
        "x5": 0.696702241897583,
        "x6": 0.36982154846191406,
    }
    correct_args_list = [
        "x1=0.1087956354022026",
        "x2=0.506428062915802",
        "x3=0.12900789082050323",
        "x4=0.3486773371696472",
        "x5=0.696702241897583",
        "x6=0.36982154846191406",
    ]
    # TODO : eps
    assert map_params_to_arg_list(params) == correct_args_list
