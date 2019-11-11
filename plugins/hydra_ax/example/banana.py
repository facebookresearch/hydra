# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="conf/config.yaml")
def banana(cfg):
    a = cfg.banana.a
    b = cfg.banana.b
    x = cfg.banana.x
    y = cfg.banana.y
    z = (a - x) ** 2 + b * (y - x ** 2) ** 2
    log.info("Banana_a_{}_b_{}({}, {})={}".format(a, b, x, y, z))
    # Return the result and the SEM, see https://ax.dev/ for more details
    return (z, 0.0)


if __name__ == "__main__":
    banana()
