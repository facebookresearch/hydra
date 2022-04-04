# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from omegaconf import DictConfig

import hydra


@hydra.main(
    version_base=None, config_path="conf", config_name="config_with_runtime_option"
)
def my_app(cfg: DictConfig) -> Any:
    print(cfg.optimizer_option)


if __name__ == "__main__":
    my_app()
