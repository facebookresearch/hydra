# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra._internal.hydra import Hydra


def test_config_installed():
    """
    Tests that color options are available for both hydra/hydra_logging and hydra/job_logging
    """
    hydra = Hydra(
        calling_file=None,
        calling_module="hydra_plugins.hydra_colorlog",
        config_path="conf/",
        task_function=None,
        strict=False,
    )
    assert "color" in hydra.config_loader.get_group_options("hydra/job_logging")
    assert "color" in hydra.config_loader.get_group_options("hydra/hydra_logging")
