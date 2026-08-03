# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(config_path="conf", config_name="config")
def my_app(_: DictConfig) -> None:
    pass


if __name__ == "__main__":
    my_app()
