# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import itertools
import logging

from hydra._internal.config_search_path import ConfigSearchPath

# TODO: Move Plugins class outside of hydra._internal
from hydra._internal.plugins import Plugins
from hydra.plugins import SearchPathPlugin, Sweeper

log = logging.getLogger(__name__)


class ExampleSweeperSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleSweeper plugin to be discovered
    and used once the ExampleSweeper plugin is installed
    """

    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-example-sweeper", "pkg://hydra_plugins.example_sweeper.conf"
        )


class ExampleSweeper(Sweeper):
    """
    Example sweeper
    """

    def __init__(self, foo, bar):
        """
        Instantiates ExampleSweeper
        """
        self.launcher = None
        self.job_results = None
        self.foo = foo
        self.bar = bar

    def setup(self, config, config_loader, task_function):
        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments):
        # Construct list of overrides per job we want to launch
        src_lists = []
        for s in arguments:
            key, value = s.split("=")
            src_lists.append(["{}={}".format(key, val) for val in value.split(",")])

        batch = list(itertools.product(*src_lists))
        log.info(
            "ExampleSweeper(foo={}, bar={}) is launching {} jobs".format(
                self.foo, self.bar, len(batch)
            )
        )
        return self.launcher.launch(batch)
