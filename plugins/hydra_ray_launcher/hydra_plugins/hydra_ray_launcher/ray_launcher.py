# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Optional, Sequence

from hydra.core.config_loader import ConfigLoader
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.types import TaskFunction
from omegaconf import DictConfig


class RayLauncher(Launcher):
    def __init__(self, ray: DictConfig) -> None:
        self.ray_cfg = ray
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        from . import _core

        return _core.launch(
            launcher=self, job_overrides=job_overrides, initial_job_idx=initial_job_idx
        )
