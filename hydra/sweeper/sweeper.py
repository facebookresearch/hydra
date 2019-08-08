"""
Sweeper plugin interface
"""
from abc import abstractmethod


class Sweeper:
    """
    An abstract sweeper interface
    Sweeper takes the command line arguments, generates a and launches jobs
    (where each job typically takes a different command line arguments)
    """

    @abstractmethod
    def setup(self, config_loader, hydra_cfg, task_function, verbose):
        """
        Setup the sweeper instance.
        :param config_loader:
        :param hydra_cfg:
        :param task_function:
        :param verbose:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def sweep(self, arguments):
        """
        Execute a sweep
        :param arguments: list of strings describing what this sweeper should do.
        exact structure is determine by the concrete Sweeper class.
        :return: the return objects of all thy launched jobs. structure depends on the Sweeper
        implementation.
        """
        raise NotImplementedError()
