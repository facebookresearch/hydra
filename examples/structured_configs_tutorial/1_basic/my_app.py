# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"


cfg_store = ConfigStore.instance()
# Registering the Config class with the name 'config'
cfg_store.store(node=MySQLConfig, name="config")


@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    # The real type of cfg is DictConfig, but we lie a little to get static type checking.
    # If it swims like a duck and quacks like a duck, it's a "duck".
    print(
        f"Connecting to {cfg.driver} at {cfg.host}:{cfg.port}, user={cfg.user}, password={cfg.password}"
    )


if __name__ == "__main__":
    my_app()
