# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys

import hydra


@hydra.main(config_path="conf/config.yaml")
def experiment(_cfg):
    print(os.getcwd())


if __name__ == "__main__":
    sys.exit(experiment())
