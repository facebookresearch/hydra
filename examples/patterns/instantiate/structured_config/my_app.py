# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, List

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import ConfigStore
from hydra.types import ObjectConf
from hydra.utils import instantiate


class DBConnection:
    def __init__(self, driver: str, host: str, port: int) -> None:
        self.driver = driver
        self.host = host
        self.port = port

    def connect(self) -> None:
        print(f"{self.driver} connecting to {self.host}:{self.port}")


class MySQLConnection(DBConnection):
    def __init__(self, driver: str, host: str, port: int) -> None:
        super().__init__(driver=driver, host=host, port=port)


class PostgreSQLConnection(DBConnection):
    def __init__(self, driver: str, host: str, port: int, timeout: int) -> None:
        super().__init__(driver=driver, host=host, port=port)
        self.timeout = timeout


@dataclass
class DBConfig:
    driver: MISSING
    host: str = "localhost"
    port: int = 80


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "MySQL"
    port: int = 1234


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "PostgreSQL"
    port: int = 5678
    timeout: int = 10


defaults = [
    # Load the config "mysql" from the config group "db"
    {"db": "mysql"}
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
    node=ObjectConf(target="my_app.MySQLConnection", params=MySQLConfig),
)
cs.store(
    group="db",
    name="postgresql",
    node=ObjectConf(target="my_app.PostgreSQLConnection", params=PostGreSQLConfig),
)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    connection = instantiate(cfg.db)
    connection.connect()


if __name__ == "__main__":
    my_app()
