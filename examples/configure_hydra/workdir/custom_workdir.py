# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys

from omegaconf import DictConfig

import hydra


@hydra.main(config_path="conf/config.yaml")
def experiment(_cfg: DictConfig) -> None:
    print(os.getcwd())


if __name__ == "__main__":
    sys.exit(experiment())
