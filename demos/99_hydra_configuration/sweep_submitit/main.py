import logging
import sys
import socket
import hydra

log = logging.getLogger(__name__)


@hydra.main()
def experiment(cfg):
    log.info("Running on: {}".format(socket.gethostname()))
    print(cfg.pretty())


if __name__ == "__main__":
    sys.exit(experiment())
