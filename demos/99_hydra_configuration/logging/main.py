import logging
import sys

import hydra

log = logging.getLogger(__name__)


@hydra.main()
def experiment(_cfg):
    log.info("Info level message")


if __name__ == "__main__":
    sys.exit(experiment())
