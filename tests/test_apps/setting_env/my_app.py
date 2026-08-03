# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

from omegaconf import DictConfig

import hydra


@hydra.main(config_name="config")
def my_app(_: DictConfig) -> None:
    print(f"foo={os.environ['foo']}")
    print(f"bar={os.environ['bar']}")


if __name__ == "__main__":
    my_app()
