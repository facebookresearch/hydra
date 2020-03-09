# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Launcher plugin interface
"""
from abc import abstractmethod
from typing import Sequence

from omegaconf import DictConfig

from hydra.core.config_loader import ConfigLoader
from hydra.core.utils import JobReturn
from hydra.types import TaskFunction

from .plugin import Plugin


class Launcher(Plugin):
    @abstractmethod
    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        """
        Sets this launcher instance up.
        """
        raise NotImplementedError()

    @abstractmethod
    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        """
        :param job_overrides: a batch of job arguments
        :param initial_job_idx: Initial job idx. used by sweepers that executes several batches
        """
        raise NotImplementedError()
