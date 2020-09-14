# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import List, Optional

from omegaconf import MISSING

from hydra.core.config_store import ConfigStore


@dataclass
class ModuleConf:
    name: str = MISSING
    classes: List[str] = MISSING


@dataclass
class ConfigenConf:

    # output dir
    output_dir: str = MISSING

    module_path_pattern: str = MISSING

    modules: List[ModuleConf] = MISSING

    # Generated file header
    header: str = MISSING


@dataclass
class Config:
    init_config_dir: Optional[str] = None
    configen: ConfigenConf = ConfigenConf()


config_store = ConfigStore.instance()
config_store.store(name="configen", node=Config)
