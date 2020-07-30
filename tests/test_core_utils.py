# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys
from typing import Any

from omegaconf import OmegaConf, open_dict

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.utils import create_config_search_path
from hydra.core import utils
from hydra.core.hydra_config import HydraConfig
from hydra.types import RunMode


def test_accessing_hydra_config(hydra_restore_singletons: Any) -> Any:
    utils.setup_globals()

    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("pkg://hydra.test_utils.configs")
    )
    cfg = config_loader.load_configuration(
        config_name="accessing_hydra_config", run_mode=RunMode.RUN, overrides=[]
    )
    HydraConfig.instance().set_config(cfg)
    with open_dict(cfg):
        del cfg["hydra"]
    assert cfg.job_name == "UNKNOWN_NAME"
    assert cfg.config_name == "accessing_hydra_config"


def test_py_version_resolver(hydra_restore_singletons: Any, monkeypatch: Any) -> Any:
    monkeypatch.setattr(sys, "version_info", (3, 7, 2))
    utils.setup_globals()
    assert OmegaConf.create({"key": "${python_version:}"}).key == "3.7"
    assert OmegaConf.create({"key": "${python_version:major}"}).key == "3"
    assert OmegaConf.create({"key": "${python_version:minor}"}).key == "3.7"
    assert OmegaConf.create({"key": "${python_version:micro}"}).key == "3.7.2"
