# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.global_hydra import GlobalHydra
from hydra.experimental import initialize
from hydra.test_utils.test_utils import chdir_plugin_root

chdir_plugin_root()


def test_config_installed() -> None:
    """
    Tests that color options are available for both hydra/hydra_logging and hydra/job_logging
    """

    with initialize(config_path="../hydra_plugins/hydra_colorlog/conf"):
        config_loader = GlobalHydra.instance().config_loader()
        assert "colorlog" in config_loader.get_group_options("hydra/job_logging")
        assert "colorlog" in config_loader.get_group_options("hydra/hydra_logging")
