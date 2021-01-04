# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

from omegaconf import DictConfig

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="conf", config_name="config")
def my_app(_cfg: DictConfig) -> None:
    # By default, only logs of warning or higher level will be printed
    log.debug("DEBUG level message")
    log.info("INFO level message")
    log.warning("WARN level message")
    log.error("ERROR level message")


if __name__ == "__main__":
    my_app()
