# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

from omegaconf import DictConfig

import hydra


@hydra.main(version_base=None)
def my_app(_cfg: DictConfig) -> None:
    print(f"Working directory : {os.getcwd()}")


if __name__ == "__main__":
    my_app()
