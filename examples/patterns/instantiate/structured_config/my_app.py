# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, List

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import ConfigStore
from hydra.types import ObjectConf


class DBConnection:
    def connect(self) -> None:
        pass


class MySQLConnection(DBConnection):
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self.driver = "MySQL"
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self) -> None:
        print(
            f"{self.driver} connecting to {self.host} with user={self.user} and password={self.password}"
        )


class PostgreSQLConnection(DBConnection):
    def __init__(
        self, host: str, port: int, user: str, password: str, database: str
    ) -> None:
        self.driver = "PostgreSQL"
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect(self) -> None:
        print(
            f"{self.driver} connecting to {self.host} with user={self.user} "
            f"and password={self.password} and database={self.database}"
        )


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 80
    user: str = MISSING
    password: str = "1234"


@dataclass
class MySQLConfig(DBConfig):
    user: str = "root"
    password: str = "1234"


@dataclass
class PostGreSQLConfig(DBConfig):
    user: str = "root"
    password: str = "1234"
    database: str = "tutorial"


defaults = [
    # Load the config "mysql" from the config group "db"
    {"db": "mysql",}
]


@dataclass
class Config(DictConfig):
    defaults: List[Any] = field(default_factory=lambda: defaults)
    db: ObjectConf = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(
    group="db",
    name="mysql",
    node=ObjectConf(target="my_app.MySQLConnection", params=MySQLConfig,),
)
cs.store(
    group="db",
    name="postgresql",
    node=ObjectConf(target="my_app.PostgreSQLConnection", params=PostGreSQLConfig,),
)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    connection = hydra.utils.instantiate(cfg.db)
    connection.connect()


if __name__ == "__main__":
    my_app()
