from abc import abstractmethod


class Sweeper:
    @abstractmethod
    def setup(self, config_loader, hydra_cfg, task_function, verbose):
        raise NotImplementedError()

    @abstractmethod
    def sweep(self, arguments):
        """
        Execute a sweep
        :param arguments: list of strings describing what this sweeper should do.
        exact structure is determine by the concrete Sweeper class.
        :return: the return objects of all thy launched jobs. structure depends on the Sweeper implementation.
        """
        raise NotImplementedError()
