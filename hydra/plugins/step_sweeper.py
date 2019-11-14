# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
A sweeper that operates on generational batches of jobs
"""

from abc import abstractmethod
from . import Sweeper
import logging

log = logging.getLogger(__name__)


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

    def setup(self, config, config_loader, task_function):
        from .._internal.plugins import Plugins

        self.config = config

        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
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
        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))

        self.arguments = arguments
        returns = []
        while not self.is_done():
            batch = self.get_job_batch()
            results = self.launcher.launch(batch)
            returns.append(results)
            self.update_results(results)
        return returns
