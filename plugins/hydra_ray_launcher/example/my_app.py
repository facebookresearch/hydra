# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig
import hydra
import logging


log = logging.getLogger(__name__)


@hydra.main(config_path="conf/config.yaml")
def my_app(cfg: DictConfig) -> None:
    log.info("Hello world from my app.")
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
