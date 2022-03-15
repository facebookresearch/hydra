# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(version_base=None)
def my_app(cfg: DictConfig) -> None:
    val = 1 / cfg.divisor
    print(f"val={val}")


if __name__ == "__main__":
    my_app()
