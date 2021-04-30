# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Optional, Sequence

from hydra.core.config_loader import ConfigLoader
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.types import TaskFunction
from omegaconf import DictConfig, OmegaConf, open_dict

from hydra_plugins.hydra_ray_launcher._config import (  # type: ignore
    RayAutoscalerConf,
    RsyncConf,
)

log = logging.getLogger(__name__)


class RayAutoScalerLauncher(Launcher):
    def __init__(
        self,
        env_setup: DictConfig,
        ray: RayAutoscalerConf,
        stop_cluster: bool,
        no_restart: bool,
        restart_only: bool,
        no_config_cache: bool,
        sync_up: RsyncConf,
        sync_down: RsyncConf,
    ) -> None:
        self.ray_cfg = ray
        self.stop_cluster = stop_cluster
        self.no_restart = no_restart
        self.restart_only = restart_only
        self.no_config_cache = no_config_cache
        self.sync_up = sync_up
        self.sync_down = sync_down
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None
        self.ray_yaml_path: Optional[str] = None
        self.env_setup = env_setup

        # Need this since the autoscaler sdk API looks for docker key
        if self.ray_cfg.cluster.docker is None:
            with open_dict(self.ray_cfg):
                OmegaConf.set_struct(self.ray_cfg.cluster, False)
                del self.ray_cfg.cluster["docker"]

        # workaround for the issue: https://github.com/ray-project/ray/issues/15096
        if self.ray_cfg.cluster.auth.ssh_private_key is None:
            with open_dict(self.ray_cfg):
                OmegaConf.set_struct(self.ray_cfg.cluster.auth, False)
                del self.ray_cfg.cluster.auth["ssh_private_key"]

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
        from . import _core_autoscaler

        return _core_autoscaler.launch(
            launcher=self, job_overrides=job_overrides, initial_job_idx=initial_job_idx
        )
