# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"


@dataclass
class PostGreSQLConfig:
    driver: str = "postgresql"
    host: str = "localhost"
    port: int = 3306
    user: str = "postgre_user"
    password: str = "drowssap"
    timeout: int = 10


@dataclass
class Config(DictConfig):
    db: Any = MISSING


cs = ConfigStore.instance()
cs.store(group="db", name="mysql", path="db", node=MySQLConfig)
cs.store(group="db", name="postgresql", path="db", node=PostGreSQLConfig)
cs.store(name="config", node=Config)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
