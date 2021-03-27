# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, List, Optional

from hydra.core.config_loader import ConfigLoader
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction
from omegaconf import DictConfig

from .config import SamplerConfig


class OptunaSweeper(Sweeper):
    """Class to interface with Optuna"""

    def __init__(
        self,
        sampler: SamplerConfig,
        direction: Any,
        storage: Optional[str],
        study_name: Optional[str],
        n_trials: int,
        n_jobs: int,
        search_space: Optional[DictConfig],
    ) -> None:
        from ._impl import OptunaSweeperImpl

        self.sweeper = OptunaSweeperImpl(
            sampler, direction, storage, study_name, n_trials, n_jobs, search_space
        )

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.sweeper.setup(config, config_loader, task_function)

    def sweep(self, arguments: List[str]) -> None:
        return self.sweeper.sweep(arguments)
