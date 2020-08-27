# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import time

import hydra
import submitit
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    env = submitit.JobEnvironment()
    log.info(f"Process ID {os.getpid()} executing task {cfg.task}, with {env}")
    time.sleep(1)


if __name__ == "__main__":
    my_app()
