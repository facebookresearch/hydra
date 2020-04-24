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


@dataclass
class Config:
    db: MySQLConfig = MySQLConfig()
    verbose: bool = True


# We no longer need to use the path parameter because Config has the correct structure
ConfigStore.instance().store(name="config", node=Config)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    # Python knows that the type of cfg.db is MySQLConfig without any additional hints
    print(
        f"Connecting to {cfg.db.driver} at {cfg.db.host}:{cfg.db.port}, "
        f"user={cfg.db.user}, password={cfg.db.password}"
    )


if __name__ == "__main__":
    my_app()
