# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.global_hydra import GlobalHydra
from hydra.core.plugins import Plugins
from hydra.experimental import initialize
from hydra.plugins.search_path_plugin import SearchPathPlugin

from hydra_plugins.example_searchpath_plugin.example_searchpath_plugin import (
    ExampleSearchPathPlugin,
)


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking at all Plugins
    assert ExampleSearchPathPlugin.__name__ in [
        x.__name__ for x in Plugins.instance().discover(SearchPathPlugin)
    ]


def test_config_installed() -> None:
    with initialize():
        config_loader = GlobalHydra.instance().config_loader()
        assert "my_default_output_dir" in config_loader.get_group_options(
            "hydra/output"
        )
