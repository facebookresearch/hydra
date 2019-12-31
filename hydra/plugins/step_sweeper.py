# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
A sweeper that operates on generational batches of jobs
"""
import logging
from abc import abstractmethod
from typing import Any, List, Optional, Sequence

from omegaconf import DictConfig

from hydra._internal.config_loader import ConfigLoader
from hydra.plugins.common.utils import JobReturn
from hydra.types import TaskFunction

from .launcher import Launcher
from .sweeper import Sweeper

log = logging.getLogger(__name__)


class StepSweeper(Sweeper):
    """
    A sweeper that support base implementation for sweepers that operates on batches
    of jobs for every generation. This may not be flexible enough for all use cases, but probably
    covers 90% of the sweeping algorithms.
    It's using an internal launcher instance to launch each batch.
    """

    def __init__(self) -> None:
        super(StepSweeper, self).__init__()
        self.arguments: Optional[List[str]] = None
        self.launcher: Optional[Launcher] = None
        self.config: Optional[DictConfig] = None

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        from .._internal.plugins import Plugins

        self.config = config

        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    @abstractmethod
    def get_job_batch(self) -> Sequence[Sequence[str]]:
        """
        :return: A list of lists of strings, each inner list is the overrides for a single job
        that should be executed.
        """
        ...

    @abstractmethod
    def is_done(self) -> bool:
        """
        :return: True if no more batch of jobs should be executed
        """
        ...

    @abstractmethod
    def update_results(self, job_results: Sequence[JobReturn]) -> None:
        """
        Update the sweeper with the outputs from the last batch of jobs. This is useful for
        sweepers that
        determine the next batch of jobs based on the results of the last batch
        :param job_results: the outputs from the last batch of jobs.
        """
        ...

    def sweep(self, arguments: List[str]) -> Any:
        assert self.config is not None
        assert self.launcher is not None
        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))

        self.arguments = arguments
        returns: List[Sequence[JobReturn]] = []
        while not self.is_done():
            batch = self.get_job_batch()
            results = self.launcher.launch(batch)
            returns.append(results)
            self.update_results(results)
        return returns
