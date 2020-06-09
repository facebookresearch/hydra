# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from omegaconf import open_dict

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.utils import create_config_search_path
from hydra.core import utils
from hydra.core.hydra_config import HydraConfig


def test_accessing_hydra_config(restore_singletons: Any) -> Any:
    utils.setup_globals()

    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("pkg://hydra.test_utils.configs")
    )
    cfg = config_loader.load_configuration(
        config_name="accessing_hydra_config", overrides=[]
    )
    HydraConfig.instance().set_config(cfg)
    with open_dict(cfg):
        del cfg["hydra"]
    assert cfg.job_name == "UNKNOWN_NAME"
    assert cfg.config_name == "accessing_hydra_config"
