# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306


@dataclass
class MyConfig:
    db: MySQLConfig = MySQLConfig()


cs = ConfigStore.instance()
cs.store(name="config", node=MyConfig)


@hydra.main(config_name="config")
def my_app(cfg: MyConfig) -> None:
    # Python knows that the type of cfg.db is MySQLConfig without any additional hints
    print(f"Host: {cfg.db.host}, port: {cfg.db.port}")


if __name__ == "__main__":
    my_app()
