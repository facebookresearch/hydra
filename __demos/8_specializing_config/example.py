# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging
import sys

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="conf/config.yaml")
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    sys.exit(experiment())
