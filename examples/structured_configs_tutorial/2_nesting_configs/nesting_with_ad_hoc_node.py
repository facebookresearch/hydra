# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306


cs = ConfigStore.instance()
cs.store(
    name="config",
    node={
        "src": MySQLConfig(host="localhost"),
        "dst": MySQLConfig(host="example.com"),
    },
)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    src: MySQLConfig = cfg.src
    dst: MySQLConfig = cfg.dst
    print(f"Copying {src.host}:{src.port} to {dst.host}:{dst.port}")


if __name__ == "__main__":
    my_app()
