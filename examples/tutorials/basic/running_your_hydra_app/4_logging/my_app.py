# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

from omegaconf import DictConfig

import hydra

# A logger for this file
log = logging.getLogger(__name__)


@hydra.main()
def my_app(_cfg: DictConfig) -> None:
    log.error("Error level message")
    log.warning("Warning level message")
    log.info("Info level message")
    log.debug("Debug level message")


if __name__ == "__main__":
    my_app()
