# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import MISSING, OmegaConf

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    encoding: str = MISSING


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    timeout: int = MISSING


@dataclass
class Config:
    db: DBConfig = MISSING


cs = ConfigStore.instance()
# we use a different group to avoid collision with the user's db group.
# Note that we use the package db to to ensure the schema is merged into the right node
cs.store(group="schema/db", name="mysql", node=MySQLConfig, package="db")
cs.store(group="schema/db", name="postgresql", node=PostGreSQLConfig, package="db")
cs.store(name="config", node=Config)


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
