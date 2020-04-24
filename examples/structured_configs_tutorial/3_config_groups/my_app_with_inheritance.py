# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class DBConfig:
    host: str = "localhost"
    driver: str = MISSING
    port: int = MISSING
    user: str = MISSING
    password: str = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver = "mysql"
    port = 3306
    user = "omry"
    password = "secret"


@dataclass
class PostGreSQLConfig(DBConfig):
    driver = "postgresql"
    port = 5432
    user = "postgre_user"
    password = "drowssap"
    # new field:
    timeout: int = 10


@dataclass
class Config(DictConfig):
    db: Any = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group="database", name="postgresql", path="db", node=PostGreSQLConfig)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
