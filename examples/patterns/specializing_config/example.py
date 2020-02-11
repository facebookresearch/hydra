# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import sys

from omegaconf import DictConfig

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="conf/config.yaml")
def experiment(cfg: DictConfig) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    sys.exit(experiment())
