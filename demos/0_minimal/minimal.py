import logging
import os
import sys

import hydra

log = logging.getLogger(__name__)

@hydra.main()
def experiment(cfg):
    log.info("CWD: {}".format(os.path.realpath(os.getcwd())))
    log.info("Configuration:\n{}".format(cfg.pretty()))


if __name__ == "__main__":
    sys.exit(experiment())
