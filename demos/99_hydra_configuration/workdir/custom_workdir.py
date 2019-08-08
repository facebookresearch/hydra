# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import sys

import hydra

log = logging.getLogger(__name__)


@hydra.main()
def experiment(_cfg):
    log.info("Working directory : {}".format(os.getcwd()))


if __name__ == "__main__":
    sys.exit(experiment())
