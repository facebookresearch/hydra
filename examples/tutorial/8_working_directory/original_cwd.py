# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

from omegaconf import DictConfig

import hydra


@hydra.main()
def my_app(_cfg: DictConfig) -> None:
    print(f"Current working directory : {os.getcwd()}")
    print(f"Orig working directory    : {hydra.utils.get_original_cwd()}")
    print(f"to_absolute_path('foo')   : {hydra.utils.to_absolute_path('foo')}")
    print(f"to_absolute_path('/foo')  : {hydra.utils.to_absolute_path('/foo')}")


if __name__ == "__main__":
    my_app()
