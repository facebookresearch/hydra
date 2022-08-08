# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import hydra
from omegaconf import DictConfig


@hydra.main(
    version_base=None, config_path=".", config_name="polynomial_with_constraint"
)
def polynomial(cfg: DictConfig) -> Any:
    x = cfg.polynomial.x
    y = cfg.polynomial.y
    z = cfg.polynomial.x
    a = 100
    b = 10
    c = 1
    result = a * (x**2) + b * y + c * z
    constraint_metric = y * x
    return {"result": result, "constraint_metric": constraint_metric}


if __name__ == "__main__":
    polynomial()
