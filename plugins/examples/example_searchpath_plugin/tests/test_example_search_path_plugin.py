# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.global_hydra import GlobalHydra
from hydra.core.plugins import Plugins
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.test_utils.test_utils import TGlobalHydraContext

from hydra_plugins.example_searchpath_plugin.example_searchpath_plugin import (
    ExampleSearchPathPlugin,
)


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking at all Plugins
    assert ExampleSearchPathPlugin.__name__ in [
        x.__name__ for x in Plugins.instance().discover(SearchPathPlugin)
    ]


def test_config_installed(hydra_global_context: TGlobalHydraContext) -> None:
    with hydra_global_context():
        config_loader = GlobalHydra.instance().config_loader()
        assert "my_default_output_dir" in config_loader.get_group_options(
            "hydra/output"
        )
