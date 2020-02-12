# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

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


ConfigStore.instance().store(node=MySQLConfig, name="config", path="db")


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    # In order to get type safety you need to tell Python that the type of cfg.db is MySQLConfig:
    db: MySQLConfig = cfg.db
    print(
        f"Connecting to {db.driver} at {db.host}:{db.port}, user={db.user}, password={db.password}"
    )


if __name__ == "__main__":
    my_app()
