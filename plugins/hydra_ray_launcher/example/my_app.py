# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra
import logging

logger = logging.getLogger(__name__)

@hydra.main(config_path="conf/config.yaml")
def my_app(cfg):
    logger.info('\n'+cfg.pretty())


if __name__ == "__main__":
    my_app()
