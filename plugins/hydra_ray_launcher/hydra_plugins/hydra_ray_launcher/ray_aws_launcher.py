# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Optional, Sequence

from hydra.core.config_loader import ConfigLoader
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.types import TaskFunction
from omegaconf import DictConfig

from hydra_plugins.hydra_ray_launcher.conf import (  # type: ignore
    RayClusterConf,
    RsyncConf,
)

log = logging.getLogger(__name__)


class RayAWSLauncher(Launcher):
    def __init__(
        self,
        mandatory_install: DictConfig,
        ray_init_cfg: DictConfig,
        ray_remote_cfg: DictConfig,
        ray_cluster_cfg: RayClusterConf,
        stop_cluster: bool,
        sync_up: RsyncConf,
        sync_down: RsyncConf,
    ) -> None:
        self.ray_init_cfg = ray_init_cfg
        self.ray_remote_cfg = ray_remote_cfg
        self.ray_cluster_cfg = ray_cluster_cfg
        self.docker_enabled = self.ray_cluster_cfg.docker.image != ""
        self.stop_cluster = stop_cluster
        self.sync_up = sync_up
        self.sync_down = sync_down
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None
        self.ray_yaml_path: Optional[str] = None
        self.mandatory_install = mandatory_install

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
