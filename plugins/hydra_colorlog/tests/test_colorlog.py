# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra._internal.hydra import GlobalHydra

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import hydra_global_context  # noqa: F401


def test_config_installed(hydra_global_context):  # noqa: F811
    """
    Tests that color options are available for both hydra/hydra_logging and hydra/job_logging
    """

    with hydra_global_context(config_dir="../hydra_plugins/hydra_colorlog/conf"):
        config_loader = GlobalHydra().hydra.config_loader
        assert "colorlog" in config_loader.get_group_options("hydra/job_logging")
        assert "colorlog" in config_loader.get_group_options("hydra/hydra_logging")
