import logging
import os
import sys

import socket

import hydra

log = logging.getLogger(__name__)

@hydra.main(config_path='conf')
def experiment(cfg):
    log.info("Running on: {}".format(socket.gethostname()))
    log.info("CWD: {}".format(os.path.realpath(os.getcwd())))
    log.info("Configuration:\n{}".format(cfg.pretty()))


if __name__ == "__main__":
    sys.exit(experiment())
