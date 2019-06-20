import logging
import os
import socket
from hydra import Task

log = logging.getLogger(__name__)


class Classify(Task):
    def setup(self, cfg):
        # Setup your experiment here, creating all members
        log.info("Running on: {}".format(socket.gethostname()))
        log.info("CWD: {}".format(os.path.realpath(os.getcwd())))
        log.info("Configuration:\n{}".format(cfg.pretty()))

    def run(self, cfg):
        # run your actual code
        pass

