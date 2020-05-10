# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, List

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


def create_list(lst: List[Any]) -> Any:
    # This helper function makes the list creation a big cleaner
    # this is unfortunately verbose due to @dataclass limitations
    return field(default_factory=lambda: list(lst))


@dataclass
class Config(DictConfig):
    defaults: List[Any] = create_list([{"database": "mysql"}])
    db: MySQLConfig = MySQLConfig()


cs = ConfigStore.instance()
cs.store(group_path="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group_path="database", name="postgresql", path="db", node=PostGreSQLConfig)
cs.store(name="config", node=Config)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
