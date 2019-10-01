# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra

# A logger for this file
log = logging.getLogger(__name__)


@hydra.main()
def my_app(_cfg):
    log.info("Info level message")
    log.debug("Debug level message")


if __name__ == "__main__":
    my_app()
