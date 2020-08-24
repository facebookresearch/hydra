# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

from omegaconf import DictConfig

import hydra


@hydra.main(config_path="conf", config_name="config")
def experiment(_cfg: DictConfig) -> None:
    print(os.getcwd())


if __name__ == "__main__":
    experiment()
