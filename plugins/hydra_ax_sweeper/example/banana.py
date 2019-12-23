# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="conf/config.yaml")
def banana(cfg):
    x = cfg.banana.x
    y = cfg.banana.y
    z = (1 - x) ** 2 + 1 * ((y - x ** 2) ** 2)
    log.info(f"Banana_Function(x={x}, y={y})={z}")
    return z


if __name__ == "__main__":
    banana()
