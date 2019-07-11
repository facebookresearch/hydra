from abc import abstractmethod


class Launcher:

    @abstractmethod
    def setup(self, config_loader, hydra_cfg, task_function, verbose, overrides):
        raise NotImplemented()

    @abstractmethod
    def launch(self):
        raise NotImplemented()
