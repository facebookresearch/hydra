# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import MISSING

from hydra.core.config_store import ConfigStore


@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = "localhost"
    port: int = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    port: int = 3306
    user: str = MISSING
    password: str = MISSING


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    user: str = MISSING
    port: int = 5432
    password: str = MISSING
    timeout: int = 10


def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(
        group="database_lib/db",
        name="mysql",
        node=MySQLConfig,
    )
    cs.store(
        group="database_lib/db",
        name="postgresql",
        node=PostGreSQLConfig,
    )
