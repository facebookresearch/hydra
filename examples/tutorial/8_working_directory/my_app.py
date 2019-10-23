# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

import hydra
from hydra import utils


@hydra.main()
def my_app(_cfg):
    print("Current working directory  : {}".format(os.getcwd()))
    print("Original working directory : {}".format(utils.get_original_cwd()))
    print("to_absolute_path('foo')    : {}".format(utils.to_absolute_path("foo")))
    print("to_absolute_path('/foo')   : {}".format(utils.to_absolute_path("/foo")))


if __name__ == "__main__":
    my_app()
