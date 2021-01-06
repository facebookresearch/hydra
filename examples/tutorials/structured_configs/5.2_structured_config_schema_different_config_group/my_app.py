# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import database_lib
from omegaconf import MISSING, OmegaConf

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class Config:
    db: database_lib.DBConfig = MISSING


cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)

# database_lib registers its configs
# in database_lib/db
database_lib.register_configs()


@hydra.main(
    config_path="conf",
    config_name="config",
)
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
