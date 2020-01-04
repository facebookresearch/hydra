# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Launcher plugin interface
"""
from abc import abstractmethod
from typing import Sequence

from omegaconf import DictConfig

from hydra._internal.config_loader import ConfigLoader
from hydra.plugins.common.utils import JobReturn
from hydra.types import TaskFunction

from .plugin import Plugin


class Launcher(Plugin):
    """
    Abstract launcher
    """

    @abstractmethod
    def __init__(self) -> None:
        ...

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
    def launch(self, job_overrides: Sequence[Sequence[str]]) -> Sequence[JobReturn]:
        """
        :param job_overrides: a batch of job arguments
        """
        raise NotImplementedError()
