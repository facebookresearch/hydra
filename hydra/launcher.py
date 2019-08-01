from abc import abstractmethod


class Launcher:

    @abstractmethod
    def setup(self, config_loader, hydra_cfg, task_function, verbose):
        raise NotImplementedError()

    @abstractmethod
    def launch(self, job_overrides):
        """
        :param job_overrides: a batch of job arguments (list<list<string>>)
        """
        raise NotImplementedError()
