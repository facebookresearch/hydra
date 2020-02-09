# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import DictConfig

import hydra
from hydra.core.structured_config_store import StructuredConfigStore


@dataclass
class DBConf:
    driver: str = "mysql"
    user: str = "omry"
    password: str = "secret"


# Registering the DBConf into the configuration named 'config' in the config path 'db'
StructuredConfigStore.instance().store(node=DBConf, name="config", path="db")


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    connect(cfg.db)


# db here is typed as DBConf
# The actual type is DictConfig but if it walks like a duck...
def connect(db: DBConf) -> None:
    print(f"Connecting to {db.driver} with user={db.user} and password={db.password}")


if __name__ == "__main__":
    my_app()
