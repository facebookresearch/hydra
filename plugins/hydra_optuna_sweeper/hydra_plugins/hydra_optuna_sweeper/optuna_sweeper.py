# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from hydra.core.config_loader import ConfigLoader
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction
from omegaconf import DictConfig

from .config import OptunaConfig


class OptunaSweeper(Sweeper):
    """Class to interface with Optuna"""

    def __init__(
        self, optuna_config: OptunaConfig, search_space: Optional[DictConfig]
    ) -> None:
        from ._impl import OptunaSweeperImpl

        self.sweeper = OptunaSweeperImpl(optuna_config, search_space)

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.sweeper.setup(config, config_loader, task_function)

    def sweep(self, arguments: List[str]) -> None:
        return self.sweeper.sweep(arguments)
