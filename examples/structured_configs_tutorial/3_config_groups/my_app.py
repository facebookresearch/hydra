# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any

from omegaconf import DictConfig

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
    port: int = 5432
    timeout: int = 10
    user: str = "postgre_user"
    password: str = "drowssap"


# Config is extending DictConfig to allow type safe access to the pretty() function below.
@dataclass
class Config(DictConfig):
    db: Any = MySQLConfig()


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group="database", name="postgresql", path="db", node=PostGreSQLConfig)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
