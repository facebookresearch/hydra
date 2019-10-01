# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

import hydra


@hydra.main()
def my_app(_cfg):
    print("Working directory : {}".format(os.getcwd()))


if __name__ == "__main__":
    my_app()
