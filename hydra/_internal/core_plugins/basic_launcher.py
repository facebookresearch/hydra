# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

from omegaconf import open_dict

from hydra._internal.pathlib import Path
from hydra.plugins.common.utils import (
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
    HydraConfig,
)
from hydra.plugins import Launcher

log = logging.getLogger(__name__)


class BasicLauncher(Launcher):
    def __init__(self):
        self.config = None
        self.config_loader = None
        self.task_function = None

    def setup(self, config, config_loader, task_function):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function

    def launch(self, job_overrides):
        setup_globals()
        configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        sweep_dir = self.config.hydra.sweep.dir
        Path(str(sweep_dir)).mkdir(parents=True, exist_ok=True)
        log.info("Launching {} jobs locally".format(len(job_overrides)))
        runs = []

        for idx, overrides in enumerate(job_overrides):
            log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(overrides))))
            sweep_config = self.config_loader.load_sweep_config(
                self.config, list(overrides)
            )
            with open_dict(sweep_config):
                sweep_config.hydra.job.id = idx
                sweep_config.hydra.job.num = idx
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
