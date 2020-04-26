# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import cast

from omegaconf import MISSING, DictConfig, OmegaConf

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = MISSING
    driver: str = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver = "mysql"
    port = 3306


@dataclass
class PostGreSQLConfig(DBConfig):
    driver = "postgresql"
    port = 5432
    timeout: int = 10


@dataclass
class Config(DictConfig):
    db: DBConfig = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group="database", name="postgresql", path="db", node=PostGreSQLConfig)


def connect_mysql(cfg: MySQLConfig) -> None:
    print(f"Connecting to MySQL: {cfg.host}:{cfg.port}")


def connect_postgresql(cfg: PostGreSQLConfig) -> None:
    print(f"Connecting to PostGreSQL: {cfg.host}:{cfg.port} (timeout={cfg.timeout})")


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    # Remember that the actual type of Config and db inside it is DictConfig.
    # If you need to get the underlying type of a config object use OmegaConf.get_type:
    if OmegaConf.get_type(cfg.db) is MySQLConfig:
        connect_mysql(cast(MySQLConfig, cfg.db))
    elif OmegaConf.get_type(cfg.db) is PostGreSQLConfig:
        connect_postgresql(cast(PostGreSQLConfig, cfg.db))
    else:
        raise ValueError()


if __name__ == "__main__":
    my_app()
