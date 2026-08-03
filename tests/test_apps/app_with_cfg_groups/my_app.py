# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from omegaconf import DictConfig

import hydra


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> Any:
    return cfg


if __name__ == "__main__":
    my_app()
