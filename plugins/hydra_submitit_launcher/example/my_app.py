# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import time

from omegaconf import DictConfig

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig):
    log.info(f"Process ID {os.getpid()} executing task {cfg.task} ...")

    time.sleep(1)


if __name__ == "__main__":
    my_app()
