from abc import abstractmethod


class Launcher:

    @abstractmethod
    def setup(self, config_loader, hydra_cfg, task_function, verbose):
        raise NotImplemented()

    @abstractmethod
    def launch(self, job_overrides):
        raise NotImplemented()
