# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from hydra import TaskFunction
from hydra.core.config_loader import ConfigLoader
from hydra.plugins.sweeper import Sweeper
from omegaconf import DictConfig

from .config import OptimConf


class NevergradSweeper(Sweeper):
    """Class to interface with the Ax Platform"""

    def __init__(self, optim: OptimConf, parametrization: Optional[DictConfig]):
        from ._impl import NevergradSweeperImpl

        self.sweeper = NevergradSweeperImpl(optim, parametrization)

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        return self.sweeper.setup(config, config_loader, task_function)

    def sweep(self, arguments: List[str]) -> None:
        return self.sweeper.sweep(arguments)
