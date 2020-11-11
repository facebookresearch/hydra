# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra
from omegaconf import DictConfig

logger = logging.getLogger(__name__)


@hydra.main(config_path="conf", config_name="config")
def sphere(cfg: DictConfig) -> float:
    x = cfg.x
    y = cfg.y
    return x ** 2 + y ** 2


if __name__ == "__main__":
    sphere()
