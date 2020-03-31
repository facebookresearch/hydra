# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import tempfile
from subprocess import PIPE, Popen
from typing import Sequence

from omegaconf import DictConfig

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.types import TaskFunction

log = logging.getLogger(__name__)


class RayAWSLauncherSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-ray-aws-launcher", "pkg://hydra_plugins.hydra_ray_aws_launcher.conf"
        )


class RayAWSLauncher(Launcher):
    def __init__(self, cluster_config: DictConfig) -> None:
        self.cluster_config = cluster_config
        self.config = None
        self.task_function = None
        self.sweep_configs = None
        self.config_loader = None

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        pass
        # self.config = config
        # self.config_loader = config_loader
        # self.task_function = task_function

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        """
        :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
        :param initial_job_idx: Initial job idx in batch.
        :return: an array of return values from run_job with indexes corresponding to the input list indexes.
        """
        # save cluster config to a temp file for ray update
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            with open(f.name, "w") as file:
                print(self.cluster_config.pretty(), file=file)

            # call 'ray up cluster.yaml' to update the cluster
            ray_up_proc = Popen(["ray", "up", f.name], stdin=PIPE, stdout=PIPE)
            # y to the prompt asking if we want to restart ray server
            ray_up_proc.communicate(input=b"y")

        # TODO add remote invocation

        return []
