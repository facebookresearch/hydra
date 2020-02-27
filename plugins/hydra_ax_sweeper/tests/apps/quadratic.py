# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from omegaconf import DictConfig, OmegaConf

import hydra


@hydra.main(config_path="quadratic.yaml")
def quadratic(cfg: DictConfig) -> Any:
    x = cfg.quadratic.x
    y = cfg.quadratic.y
    a = 100
    b = 1
    z = a * (x ** 2) + b * y
    return z


if __name__ == "__main__":
    quadratic()
