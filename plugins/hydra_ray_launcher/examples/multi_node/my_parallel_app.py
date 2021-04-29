# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import socket
import time

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(config_path="./config", config_name="my_parallel_app")
def my_app(cfg: DictConfig) -> None:
    host = socket.gethostbyname(socket.gethostname())
    log.info(f"Executing task {cfg.task} on node with IP {host}")

    time.sleep(60)


if __name__ == "__main__":
    my_app()
