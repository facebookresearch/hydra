# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Launcher plugin interface
"""
from abc import abstractmethod
from .plugin import Plugin


class Launcher(Plugin):
    """
    Abstract launcher
    """

    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def setup(self, config, config_loader, task_function):
        """
        Sets this launcher instance up.
        """
        raise NotImplementedError()

    @abstractmethod
    def launch(self, job_overrides):
        """
        :param job_overrides: a batch of job arguments (list<list<string>>)
        """
        raise NotImplementedError()
