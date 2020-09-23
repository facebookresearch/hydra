# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import hydra
from omegaconf import DictConfig


@hydra.main(config_name="polynomial_with_dict_coefficients")
def polynomial_with_dict_coefficients(cfg: DictConfig) -> Any:
    c = cfg.polynomial.coefficients
    x, y, z = c["x"], c["y"], c["z"]
    a = 100
    b = 10
    c = 1
    return a * (x ** 2) + b * y + c * z


if __name__ == "__main__":
    polynomial_with_dict_coefficients()
