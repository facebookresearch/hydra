# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306


cfg_store = ConfigStore.instance()
# Registering the Config class with the name 'config'
cfg_store.store(node=MySQLConfig, name="config")


@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    if cfg.post == "localhost":
        print("Home is where the heart is!")


if __name__ == "__main__":
    my_app()
