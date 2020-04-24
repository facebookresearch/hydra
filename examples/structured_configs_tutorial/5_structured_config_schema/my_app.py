# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import MISSING, DictConfig

import hydra
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


# registering db/mysql and db/postgresql schemas.
cs = ConfigStore.instance()
cs.store(group="db", name="mysql", path="db", node=MySQLConfig, provider="main")
cs.store(
    group="db", name="postgresql", path="db", node=PostGreSQLConfig, provider="main"
)


# config here is config.yaml under the conf directory.
# config.yaml will compose in db: mysql by default (per the defaults list),
# and it will be validated against the schema
@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
