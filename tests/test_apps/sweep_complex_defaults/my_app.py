# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(config_path="conf", config_name="config")
def my_app(_cfg: DictConfig) -> None:
    print(_cfg.pretty())


if __name__ == "__main__":
    my_app()
