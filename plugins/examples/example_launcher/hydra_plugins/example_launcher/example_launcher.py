# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

from omegaconf import open_dict

from hydra._internal.config_search_path import ConfigSearchPath
from hydra._internal.pathlib import Path
from hydra.plugins import Launcher
from hydra.plugins import SearchPathPlugin
from hydra.plugins.common.utils import (
    configure_log,
    get_overrides_dirname,
    filter_overrides,
    run_job,
    setup_globals,
    HydraConfig,
)

log = logging.getLogger(__name__)


class ExampleLauncherSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleLauncher plugin to be discovered
    and used once the ExampleLauncher plugin is installed
    """

    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-example-launcher", "pkg://hydra_plugins.example_launcher.conf"
        )


class ExampleLauncher(Launcher):
    def __init__(self, foo, bar):
        self.config = None
        self.config_loader = None
        self.task_function = None
        # foo and var are coming from the the plugin's configuration
        self.foo = foo
        self.bar = bar

    def setup(self, config, config_loader, task_function):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function

    def launch(self, job_overrides):
        """
        :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
        :return: an array of return values from run_job with indexes corresponding to the input list indexes.
        """
        setup_globals()
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
                sweep_config.hydra.job.override_dirname = get_overrides_dirname(
                    sweep_config.hydra.overrides.task
                )
            HydraConfig().set_config(sweep_config)

            ret = run_job(
                config=sweep_config,
                task_function=self.task_function,
                job_dir_key="hydra.sweep.dir",
                job_subdir_key="hydra.sweep.subdir",
            )
            runs.append(ret)
            configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        return runs
