# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import hydra
from omegaconf import DictConfig


@hydra.main(config_name="polynomial_with_dict_coefficients")
def polynomial_with_dict_coefficients(cfg: DictConfig) -> Any:
    coefficients = cfg.polynomial.coefficients
    print(coefficients)
    breakpoint()
    x, y, z = coefficients[x], coefficients[y], coefficients[z]
    a = 100
    b = 10
    c = 1
    result = a * (x ** 2) + b * y + c * z
    return result


if __name__ == "__main__":
    polynomial_with_dict_coefficients()
