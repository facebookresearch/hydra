# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Sweeper plugin interface
"""
from abc import abstractmethod

from .._internal.plugins import Plugins


class Sweeper(object):
    """
    An abstract sweeper interface
    Sweeper takes the command line arguments, generates a and launches jobs
    (where each job typically takes a different command line arguments)
    """

    def __init__(self):
        if type(self) == Sweeper:
            raise NotImplementedError

    @abstractmethod
    def setup(self, config, config_loader, task_function, verbose):
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


"""
A sweeper that operates on generational batches of jobs
"""


class StepSweeper(Sweeper):
    """
    A sweeper that support base implementation for sweepers that operates on batches
    of jobs for every generation. This may not be flexible enough for all use cases, but probably
    covers 90% of the sweeping algorithms.
    It's using an internal launcher instance to launch each batch.
    """

    def __init__(self):
        super(StepSweeper, self).__init__()
        self.arguments = None
        self.launcher = None

    def setup(self, config, config_loader, task_function, verbose):
        self.launcher = Plugins.instantiate_launcher(
            config=config,
            config_loader=config_loader,
            task_function=task_function,
            verbose=verbose,
        )

    @abstractmethod
    def get_job_batch(self):
        """
        :return: A list of lists of strings, each inner list is the overrides for a single job
        that should be executed.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_done(self):
        """
        :return: True if no more batch of jobs should be executed
        """
        raise NotImplementedError()

    @abstractmethod
    def update_results(self, job_results):
        """
        Update the sweeper with the outputs from the last batch of jobs. This is useful for
        sweepers that
        determine the next batch of jobs based on the results of the last batch
        :param job_results: the outputs from the last batch of jobs.
        """
        raise NotImplementedError()

    def sweep(self, arguments):
        self.arguments = arguments
        returns = []
        while not self.is_done():
            batch = self.get_job_batch()
            results = self.launcher.launch(batch)
            returns.append(results)
            self.update_results(results)
        return returns
