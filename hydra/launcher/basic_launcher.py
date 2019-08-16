# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import six
from omegaconf import open_dict

from hydra import utils
from .launcher import Launcher

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

log = logging.getLogger(__name__)


class BasicLauncher(Launcher):
    def __init__(self):
        self.config = None
        self.config_loader = None
        self.task_function = None
        self.verbose = None

    def setup(self, config, config_loader, task_function, verbose):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function
        self.verbose = verbose

    def launch(self, job_overrides):
        utils.setup_globals()
        utils.configure_log(self.config.hydra.hydra_logging, self.verbose)
        sweep_dir = self.config.hydra.sweep.dir
        Path(str(sweep_dir)).mkdir(parents=True, exist_ok=True)
        log.info("Launching {} jobs locally".format(len(job_overrides)))
        log.info("Sweep output dir : {}".format(sweep_dir))
        runs = []

        for idx, overrides in enumerate(job_overrides):
            log.info(
                "\t#{} : {}".format(idx, " ".join(utils.filter_overrides(overrides)))
            )
            sweep_config = self.config_loader.load_sweep_config(
                self.config, list(overrides)
            )
            with open_dict(sweep_config):
                sweep_config.hydra.job.id = idx
                sweep_config.hydra.job.num = idx
                sweep_config.hydra.job.override_dirname = utils.get_overrides_dirname(
                    sweep_config.hydra.overrides.task
                )
            utils.HydraConfig().set_config(sweep_config)

            runs.append(
                utils.run_job(
                    config=sweep_config,
                    task_function=self.task_function,
                    verbose=self.verbose,
                    job_dir_key="hydra.sweep.dir",
                    job_subdir_key="hydra.sweep.subdir",
                )
            )
            utils.configure_log(self.config.hydra.hydra_logging, self.verbose)
        return runs
