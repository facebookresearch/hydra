from hydra import Task


class Task2(Task):
    def __init__(self):
        self.log = None
        self.cfg = None

    def setup(self, log, cfg):
        self.log = log
        self.log.info("Task2 setup")

    def run(self, cfg):
        self.log.info("Task2 run")
        self.log.info("Config:\n{}".format(cfg.pretty()))

