# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction
from omegaconf import DictConfig


class AxSweeperSearchPathPlugin(SearchPathPlugin):
    """
    This plugin makes the config files (provided by the AxSweeper plugin) discoverable and
    useable by the AxSweeper plugin.
    """

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-ax-sweeper", "pkg://hydra_plugins.hydra_ax_sweeper.conf"
        )


class AxSweeper(Sweeper):
    """Class to interface with the Ax Platform"""

    def __init__(self, ax_config: DictConfig, max_batch_size: Optional[int]):
        from ._core import CoreAxSweeper

        self.sweeper = CoreAxSweeper(ax_config, max_batch_size)

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        return self.sweeper.setup(config, config_loader, task_function)

    def sweep(self, arguments: List[str]) -> None:
        return self.sweeper.sweep(arguments)
