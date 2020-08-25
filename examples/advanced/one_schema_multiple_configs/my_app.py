# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf, MISSING


@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = MISSING
    user: str = MISSING
    password: str = MISSING


@dataclass
class Config:
    db: DBConfig = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=Config)


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
