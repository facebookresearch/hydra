# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Optional, Sequence

from hydra.core.config_loader import ConfigLoader
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.types import TaskFunction
from omegaconf import DictConfig

from hydra_plugins.hydra_ray_launcher._config import (  # type: ignore
    RayAWSConf,
    RsyncConf,
)

log = logging.getLogger(__name__)


class RayAWSLauncher(Launcher):
    def __init__(
        self,
        env_setup: DictConfig,
        ray: RayAWSConf,
        stop_cluster: bool,
        sync_up: RsyncConf,
        sync_down: RsyncConf,
    ) -> None:
        self.ray_cfg = ray
        self.stop_cluster = stop_cluster
        self.sync_up = sync_up
        self.sync_down = sync_down
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None
        self.ray_yaml_path: Optional[str] = None
        self.env_setup = env_setup

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
        from . import _core_aws

        return _core_aws.launch(
            launcher=self, job_overrides=job_overrides, initial_job_idx=initial_job_idx
        )
