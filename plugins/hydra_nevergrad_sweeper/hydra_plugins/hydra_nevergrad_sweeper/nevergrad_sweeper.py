# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Optional, List

from hydra_plugins.hydra_nevergrad_sweeper.config import OptimConf
from omegaconf import DictConfig

from hydra import TaskFunction
from hydra.core.config_loader import ConfigLoader
from hydra.plugins.sweeper import Sweeper


class NevergradSweeper(Sweeper):
    """Class to interface with the Ax Platform"""

    def __init__(
        self, optim: OptimConf, version: int, parametrization: Optional[DictConfig]
    ):
        from .core import CoreNevergradSweeper

        self.sweeper = CoreNevergradSweeper(optim, version, parametrization)

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        return self.sweeper.setup(config, config_loader, task_function)

    def sweep(self, arguments: List[str]) -> None:
        return self.sweeper.sweep(arguments)
