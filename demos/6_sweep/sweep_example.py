import logging
import socket
import sys

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    log.info("Running on: {}".format(socket.gethostname()))
    log.info(cfg.pretty())


if __name__ == "__main__":
    sys.exit(experiment())
