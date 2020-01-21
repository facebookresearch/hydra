# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any

from omegaconf import DictConfig

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="conf/config.yaml")
def banana(cfg: DictConfig) -> Any:
    x = cfg.banana.x
    y = cfg.banana.y
    a = 1
    b = 1
    z = (a - x) ** 2 + b * ((y - x ** 2) ** 2)
    log.info(f"Banana_Function(x={x}, y={y})={z}")
    return z


if __name__ == "__main__":
    banana()
