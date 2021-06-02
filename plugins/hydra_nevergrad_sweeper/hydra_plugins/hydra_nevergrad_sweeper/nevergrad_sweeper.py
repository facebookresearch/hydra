# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from hydra import TaskFunction
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext
from omegaconf import DictConfig

from .config import OptimConf


class NevergradSweeper(Sweeper):
    """Class to interface with Nevergrad"""

    def __init__(self, optim: OptimConf, parametrization: Optional[DictConfig]):
        from ._impl import NevergradSweeperImpl

        self.sweeper = NevergradSweeperImpl(optim, parametrization)

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        return self.sweeper.setup(
            hydra_context=hydra_context, task_function=task_function, config=config
        )

    def sweep(self, arguments: List[str]) -> None:
        return self.sweeper.sweep(arguments)
