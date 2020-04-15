# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from pathlib import Path
from typing import Optional, Sequence

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.hydra_config import HydraConfig
from hydra.core.utils import (
    JobReturn,
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
)
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.types import TaskFunction
from omegaconf import DictConfig, open_dict

# IMPORTANT:
# If your plugin imports any module that takes more than a fraction of a second to import,
# Import the module lazily (typically inside launch()).
# Installed plugins are imported during Hydra initialization and plugins that are slow to import plugins will slow
# the startup of ALL hydra applications.


log = logging.getLogger(__name__)


class ExampleLauncherSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleLauncher plugin to be discovered
    and used once the ExampleLauncher plugin is installed
    """

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-example-launcher", "pkg://hydra_plugins.example_launcher_plugin.conf"
        )


class ExampleLauncher(Launcher):
    def __init__(self, foo: str, bar: str) -> None:
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None

        # foo and var are coming from the the plugin's configuration
        self.foo = foo
        self.bar = bar

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
        """
        :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
        :param initial_job_idx: Initial job idx in batch.
        :return: an array of return values from run_job with indexes corresponding to the input list indexes.
        """
        setup_globals()
        assert self.config is not None
        assert self.config_loader is not None
        assert self.task_function is not None

        configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        sweep_dir = Path(str(self.config.hydra.sweep.dir))
        sweep_dir.mkdir(parents=True, exist_ok=True)
        log.info(
            "Example Launcher(foo={}, bar={}) is launching {} jobs locally".format(
                self.foo, self.bar, len(job_overrides)
            )
        )
        log.info("Sweep output dir : {}".format(sweep_dir))
        runs = []

        for idx, overrides in enumerate(job_overrides):
            idx = initial_job_idx + idx
            log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(overrides))))
            sweep_config = self.config_loader.load_sweep_config(
                self.config, list(overrides)
            )
            with open_dict(sweep_config):
                # This typically coming from the underlying scheduler (SLURM_JOB_ID for instance)
                # In that case, it will not be available here because we are still in the main process.
                # but instead should be populated remotely before calling the task_function.
                sweep_config.hydra.job.id = "job_id_for_{}".format(idx)
                sweep_config.hydra.job.num = idx
            HydraConfig.instance().set_config(sweep_config)

            ret = run_job(
                config=sweep_config,
                task_function=self.task_function,
                job_dir_key="hydra.sweep.dir",
                job_subdir_key="hydra.sweep.subdir",
            )
            runs.append(ret)
            # reconfigure the logging subsystem for Hydra as the run_job call configured it for the Job.
            # This is needed for launchers that calls run_job in the same process and not spawn a new one.
            configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        return runs
