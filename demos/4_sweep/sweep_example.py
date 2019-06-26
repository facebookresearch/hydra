import logging
import os
import socket
import sys

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    log.info("Running on: {}".format(socket.gethostname()))
    log.info("CWD: {}".format(os.path.realpath(os.getcwd())))
    log.info("Configuration:\n{}".format(cfg.pretty()))
    # for item, value in os.environ.items():
    #     log.info('{}={}'.format(item, value))


if __name__ == "__main__":
    sys.exit(experiment())
