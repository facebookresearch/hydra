# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Sweeper plugin interface
"""
from abc import abstractmethod

from .plugin import Plugin


class Sweeper(Plugin):
    """
    An abstract sweeper interface
    Sweeper takes the command line arguments, generates a and launches jobs
    (where each job typically takes a different command line arguments)
    """

    def __init__(self):
        if type(self) == Sweeper:
            raise NotImplementedError

    @abstractmethod
    def setup(self, config, config_loader, task_function):
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
