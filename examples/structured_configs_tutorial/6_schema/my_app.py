# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import SchemaStore


@dataclass
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    user: str = MISSING
    password: str = MISSING


@dataclass
class PostGreSQLConfig:
    driver: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    timeout: int = 10
    user: str = MISSING
    password: str = MISSING


ss = SchemaStore.instance()
ss.store(group="db", name="mysql", path="db", node=MySQLConfig)
ss.store(group="db", name="postgresql", path="db", node=PostGreSQLConfig)


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
