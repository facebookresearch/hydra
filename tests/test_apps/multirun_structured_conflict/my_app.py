# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class TestConfig:
    param: int = MISSING


config_store = ConfigStore.instance()
config_store.store(group="test", name="default", node=TestConfig)


@hydra.main(config_name="config")
def run(config: DictConfig):
    print(config.test.param)


if __name__ == "__main__":
    run()
