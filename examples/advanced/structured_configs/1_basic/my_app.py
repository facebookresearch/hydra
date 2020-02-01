# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.structured_config_store import StructuredConfigStore


@dataclass
class DBConf:
    driver: str = "mysql"
    user: str = "omry"
    password: str = "secret"


@dataclass
class AppConfig:
    db: DBConf = DBConf()


StructuredConfigStore.instance().store(
    group=None, name="config", path="", node=AppConfig
)


@hydra.main(config_path="config.yaml")
def my_app(cfg: AppConfig) -> None:
    print(f"driver : {cfg.db.driver}")
    print(f"user : {cfg.db.user}")
    print(f"password : {cfg.db.password}")


if __name__ == "__main__":
    my_app()
