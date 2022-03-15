# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

from omegaconf import DictConfig

import hydra

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(_cfg: DictConfig) -> None:
    log.info("Info level message")


if __name__ == "__main__":
    my_app()
