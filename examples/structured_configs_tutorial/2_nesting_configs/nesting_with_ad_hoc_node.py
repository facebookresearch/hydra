# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306


cfg_store = ConfigStore.instance()
cfg_store.store(name="config", node={"db": MySQLConfig})


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    db: MySQLConfig = cfg.db
    print(f"Host: {db.host}, port: {db.port}")


if __name__ == "__main__":
    my_app()
