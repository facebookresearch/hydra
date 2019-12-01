# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="conf/config.yaml")
def banana(cfg):
    print(cfg)
    a = cfg.banana.a
    b = cfg.banana.b
    x = cfg.banana.x
    y = cfg.banana.y
    z = (a - x) ** 2 + b * ((y - x ** 2) ** 2)
    log.info(f"Banana_Function_a={a}_b={b}(x={x}, y={y})={z}")
    return z


if __name__ == "__main__":
    banana()
