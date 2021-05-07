# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import time

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(config_path='./config', config_name="main")
def my_app(cfg: DictConfig) -> None:
    log.info(f"Executing task {cfg.task}")
    module = hydra.utils.instantiate(cfg.module)
    log.info(repr(module))
    time.sleep(1)


if __name__ == "__main__":
    my_app()
