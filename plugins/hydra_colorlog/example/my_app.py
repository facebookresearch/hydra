# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra

# A logger for this file
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(config_name="config")
def my_app(_cfg: DictConfig) -> None:
    log.debug("Debug level message")
    log.info("Info level message")
    log.warning("Warning level message")
    log.error("Error level message")
    log.critical("Critical level message")


if __name__ == "__main__":
    my_app()
