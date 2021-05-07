# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Optional, Sequence

from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.types import HydraContext, TaskFunction
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
        log_style: str,
        color_mode: str,
        verbosity: int,
        update_cluster_no_restart: bool,
        update_cluster_restart_only: bool,
        update_cluster_no_config_cache: bool,
        teardown_workers_only: bool,
        teardown_keep_min_workers: bool,
    ) -> None:
        self.ray_cfg = ray
        self.stop_cluster = stop_cluster
        self.sync_up = sync_up
        self.sync_down = sync_down
        self.log_style = log_style
        self.color_mode = color_mode
        self.verbosity = verbosity
        self.update_cluster_no_restart = update_cluster_no_restart
        self.update_cluster_restart_only = update_cluster_restart_only
        self.update_cluster_no_config_cache = update_cluster_no_config_cache
        self.teardown_workers_only = teardown_workers_only
        self.teardown_keep_min_workers = teardown_keep_min_workers
        self.config: Optional[DictConfig] = None
        self.hydra_context: Optional[HydraContext] = None
        self.task_function: Optional[TaskFunction] = None
        self.ray_yaml_path: Optional[str] = None
        self.env_setup = env_setup

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.config = config
        self.hydra_context = hydra_context
        self.task_function = task_function

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        from . import _core_aws

        return _core_aws.launch(
            launcher=self, job_overrides=job_overrides, initial_job_idx=initial_job_idx
        )
