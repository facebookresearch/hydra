# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

from omegaconf import DictConfig

import hydra


@hydra.main()
def my_app(_cfg: DictConfig) -> None:
    print("Current working directory : {}".format(os.getcwd()))
    print("Orig working directory    : {}".format(hydra.utils.get_original_cwd()))
    print("to_absolute_path('foo')   : {}".format(hydra.utils.to_absolute_path("foo")))
    print("to_absolute_path('/foo')  : {}".format(hydra.utils.to_absolute_path("/foo")))


if __name__ == "__main__":
    my_app()
