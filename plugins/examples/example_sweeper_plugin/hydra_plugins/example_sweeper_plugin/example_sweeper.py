# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import itertools
import logging
from typing import Any, List, Optional

from omegaconf import DictConfig

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction

log = logging.getLogger(__name__)


class ExampleSweeperSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleSweeper plugin to be discovered
    and used once the ExampleSweeper plugin is installed
    """

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-example-sweeper", "pkg://hydra_plugins.example_sweeper_plugin.conf"
        )


class ExampleSweeper(Sweeper):
    def __init__(self, foo: str, bar: str):
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        self.job_results = None
        self.foo = foo
        self.bar = bar

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.config = config
        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments: List[str]) -> Any:
        assert self.config is not None
        assert self.launcher is not None
        log.info("ExampleSweeper (foo={}, bar={}) sweeping".format(self.foo, self.bar))
        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))
        # Construct list of overrides per job we want to launch
        src_lists = []
        for s in arguments:
            key, value = s.split("=")
            # for each argument, create a list. if the argument has , (aka - is a sweep), add an element for each
            # option to that list, otherwise add a single element with the value
            src_lists.append(["{}={}".format(key, val) for val in value.split(",")])

        batch = list(itertools.product(*src_lists))

        returns = [self.launcher.launch(batch)]
        return returns
