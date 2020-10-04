# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import DictConfig, OmegaConf

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    host: str
    port: int
    user: str
    password: str
    driver: str = "mysql"


@dataclass
class PostGreSQLConfig:
    host: str
    port: int
    timeout: int
    user: str
    password: str
    driver: str = "postgresql"


cs = ConfigStore.instance()
cs.store(group="schema/db", name="mysql", node=MySQLConfig, package="db")
cs.store(group="schema/db", name="postgresql", node=PostGreSQLConfig, package="db")


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
