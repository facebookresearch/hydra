# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import hydra
from omegaconf import DictConfig


@hydra.main(config_name="polynomial_with_dict_coefficients")
def polynomial_with_dict_coefficients(cfg: DictConfig) -> Any:
    coeff = cfg.polynomial.coefficients
    a = 100
    b = 10
    c = 1
    return a * (coeff.x ** 2) + b * coeff.y + c * coeff.z


if __name__ == "__main__":
    polynomial_with_dict_coefficients()
