# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306


cs = ConfigStore.instance()
# Registering the Config class with the name 'config'.
cs.store(name="config", node=MySQLConfig)


@hydra.main(version_base=None, config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    print(f"Host: {cfg.host}, port: {cfg.port}")


if __name__ == "__main__":
    my_app()
