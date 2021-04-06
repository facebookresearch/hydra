# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import hydra
from omegaconf import DictConfig


@hydra.main(config_path=".", config_name="polynomial")
def polynomial(cfg: DictConfig) -> Any:
    x = cfg.polynomial.x
    y = cfg.polynomial.y
    z = cfg.polynomial.x
    a = 100
    b = 10
    c = 1
    result = a * (x ** 2) + b * y + c * z
    return result


if __name__ == "__main__":
    polynomial()
