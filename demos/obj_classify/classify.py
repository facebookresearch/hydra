import logging

from hydra import Task

log = logging.getLogger(__name__)


class Classify(Task):
    def setup(self, cfg):
        # Setup your experiment here, creating all members
        log.info("Classify.setup")

    def run(self, cfg):
        log.info("Classify.run, config:\n\n{}".format(cfg.pretty()))

