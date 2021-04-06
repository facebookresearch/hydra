# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import hydra
from omegaconf import DictConfig


@hydra.main(config_path=".", config_name="polynomial_with_coefficients")
def polynomial_with_list_coefficients(cfg: DictConfig) -> Any:
    x, y, z = cfg.polynomial.coefficients
    a = 100
    b = 10
    c = 1
    return a * (x ** 2) + b * y + c * z


if __name__ == "__main__":
    polynomial_with_list_coefficients()
