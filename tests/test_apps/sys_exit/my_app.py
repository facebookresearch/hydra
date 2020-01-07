# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys

from omegaconf import DictConfig

import hydra


@hydra.main()
def my_app(_: DictConfig) -> None:
    sys.exit(42)


if __name__ == "__main__":
    my_app()
