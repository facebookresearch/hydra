# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import MISSING, OmegaConf

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = MISSING
    driver: str = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    port: int = 3306


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    port: int = 5432
    timeout: int = 10


@dataclass
class Config:
    # We can now annotate db as DBConfig which
    # improves both static and dynamic type safety.
    db: DBConfig


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)


@hydra.main(version_base=None, config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
