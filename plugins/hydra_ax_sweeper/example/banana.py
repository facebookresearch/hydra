# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(config_path="conf", config_name="config")
def banana(cfg: DictConfig) -> Any:
    x = cfg.banana.x
    y = cfg.banana.y
    a = 1
    b = 100
    z = (a - x) ** 2 + b * ((y - x ** 2) ** 2)
    log.info(f"Banana_Function(x={x}, y={y})={z}")
    return z


if __name__ == "__main__":
    banana()
