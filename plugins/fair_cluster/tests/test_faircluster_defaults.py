# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra._internal.plugins import Plugins
from hydra.plugins import SearchPathPlugin
from hydra_plugins.fair_cluster.fair_cluster_defaults import FAIRClusterDefaults


def test_discovery():
    launchers = Plugins.discover(SearchPathPlugin)
    # discovered plugins are actually different class objects, compare by name
    assert FAIRClusterDefaults.__name__ in [x.__name__ for x in launchers]


def test_fair_cluster_defaults():
    pass
