from hydra import Task


class Task1(Task):
    def __init__(self):
        self.log = None
        self.cfg = None

    def setup(self, log, cfg):
        self.log = log
        self.log.info("Task1 setup")

    def run(self, cfg):
        self.log.info("Task1 run")
        self.log.info("Config:\n{}".format(cfg.pretty()))
