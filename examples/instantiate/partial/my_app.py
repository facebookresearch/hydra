# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from omegaconf import DictConfig

import hydra
from hydra.utils import instantiate


class Optimizer:
    algo: str
    lr: float

    def __init__(self, algo: str, lr: float) -> None:
        self.algo = algo
        self.lr = lr

    def __repr__(self) -> str:
        return f"Optimizer(algo={self.algo},lr={self.lr})"


class Model:
    def __init__(self, optim_partial: Any, lr: float):
        super().__init__()
        self.optim = optim_partial(lr=lr)
        self.lr = lr

    def __repr__(self) -> str:
        return f"Model(Optimizer={self.optim},lr={self.lr})"


@hydra.main(config_path=".", config_name="config")
def my_app(cfg: DictConfig) -> None:
    model = instantiate(cfg.model)
    print(model)


if __name__ == "__main__":
    my_app()
