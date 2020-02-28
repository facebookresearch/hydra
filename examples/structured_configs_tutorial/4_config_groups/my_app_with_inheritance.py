# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = "localhost"
    port: int = MISSING
    user: str = MISSING
    password: str = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    port: int = 5432
    timeout: int = 10
    user: str = "postgre_user"
    password: str = "drowssap"


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
