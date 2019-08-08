# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Launcher plugin interface
"""
from abc import abstractmethod


class Launcher:
    """
    Abstract launcher
    """

    @abstractmethod
    def setup(self, config_loader, hydra_cfg, task_function, verbose):
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
