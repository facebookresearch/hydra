# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main()
def my_app(_: DictConfig) -> None:
    1 / 0


if __name__ == "__main__":
    my_app()
