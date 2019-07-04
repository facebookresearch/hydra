from abc import abstractmethod


class Launcher:

    @abstractmethod
    def setup(self, cfg_dir, cfg_filename, hydra_cfg, task_function, verbose, overrides):
        raise NotImplemented()

    @abstractmethod
    def launch(self):
        raise NotImplemented()
