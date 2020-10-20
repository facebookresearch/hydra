# Copyright (c) 2020 Facebook, Inc. and its affiliates. All Rights Reserved
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from typing import List, Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING


@dataclass
class ModuleConf:
    # Optional: URL - link to the documentation of a given module.
    url: Optional[str] = None
    # Name of the module.
    name: str = MISSING
    # List of classes of a given module.
    classes: List[str] = MISSING


@dataclass
class ConfigenConf:

    # output dir
    output_dir: str = MISSING

    module_path_pattern: str = MISSING

    modules: List[ModuleConf] = MISSING

    # Generated file header.
    header: str = MISSING


@dataclass
class Config:
    init_config_dir: Optional[str] = None
    configen: ConfigenConf = ConfigenConf()


config_store = ConfigStore.instance()
config_store.store(name="configen", node=Config)
