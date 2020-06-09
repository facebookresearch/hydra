# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any, Optional, Sequence

from hydra.core.config_loader import ConfigLoader
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.types import TaskFunction
from omegaconf import DictConfig

log = logging.getLogger(__name__)


class JoblibLauncher(Launcher):
    def __init__(self, **kwargs: Any) -> None:
        """Joblib Launcher

        Launches parallel jobs using Joblib.Parallel. For details, refer to:
        https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html

        This plugin is based on the idea and inital implementation of @emilemathieutmp:
        https://github.com/facebookresearch/hydra/issues/357
        """
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None

        self.joblib = kwargs

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
