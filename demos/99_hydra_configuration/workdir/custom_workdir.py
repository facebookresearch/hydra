import logging
import os
import sys

import hydra

# pylint: disable=C0103
log = logging.getLogger(__name__)


@hydra.main()
def experiment(_cfg):
    log.info(f"Working directory : {os.getcwd()}")


if __name__ == "__main__":
    sys.exit(experiment())
