# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os

import hydra._internal.utils
import hydra.plugins.common.utils
from hydra.plugins import Launcher

from omegaconf import open_dict

# pylint: disable=C0103
log = logging.getLogger(__name__)


class SubmititLauncher(Launcher):
    def __init__(self, queue, folder, queue_parameters, conda_file=None):
        self.queue = queue
        self.queue_parameters = queue_parameters
        self.folder = folder
        self.conda_file = conda_file
        self.config = None
        self.task_function = None
        self.verbose = None
        self.sweep_configs = None
        self.config_loader = None

    def setup(self, config, config_loader, task_function, verbose):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function
        self.verbose = verbose

    def launch_job(self, sweep_overrides, job_dir_key, job_num, singleton_state):
        hydra.plugins.common.utils.Singleton.set_state(singleton_state)
        hydra.plugins.common.utils.configure_log(None, self.verbose)
        hydra.plugins.common.utils.setup_globals()
        sweep_config = self.config_loader.load_sweep_config(
            self.config, sweep_overrides
        )
        with open_dict(sweep_config):
            # Populate new job variables
            if "SLURM_JOB_ID" in os.environ:
                sweep_config.hydra.job.id = os.environ["SLURM_JOB_ID"]
            elif "CHRONOS_JOB_ID" in os.environ:
                sweep_config.hydra.job.id = os.environ["CHRONOS_JOB_ID"]
            else:
                sweep_config.hydra.job.id = "unknown"

            sweep_config.hydra.job.num = job_num
            sweep_config.hydra.job.override_dirname = hydra.plugins.common.utils.get_overrides_dirname(
                sweep_config.hydra.overrides.task
            )

        return hydra.plugins.common.utils.run_job(
            config=sweep_config,
            task_function=self.task_function,
            verbose=self.verbose,
            job_dir_key=job_dir_key,
            job_subdir_key="hydra.sweep.subdir",
        )

    def launch(self, job_overrides):
        # lazy import to ensure plugin discovery remains fast
        import submitit

        num_jobs = len(job_overrides)
        assert num_jobs > 0
        with open_dict(self.config):
            self.config.hydra.job.num_jobs = num_jobs

        if self.queue == "auto":
            executor = submitit.AutoExecutor(
                folder=self.folder, conda_file=self.conda_file
            )
        elif self.queue == "slurm":
            executor = submitit.SlurmExecutor(folder=self.folder)
        elif self.queue == "chronos":
            executor = submitit.ChronosExecutor(
                folder=self.folder, conda_file=self.conda_file
            )
        elif self.queue == "local":
            executor = submitit.LocalExecutor(folder=self.folder)
        else:
            raise RuntimeError("Unsupported queue type {}".format(self.queue))

        executor.update_parameters(**self.queue_parameters[self.queue])

        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))
        path_str = str(self.config.hydra.sweep.dir)
        os.makedirs(path_str, exist_ok=True)
        if "mode" in self.config.hydra.sweep:
            mode = int(str(self.config.hydra.sweep.mode), 8)
            os.chmod(path_str, mode=mode)

        jobs = []
        for job_num in range(num_jobs):
            sweep_override = list(job_overrides[job_num])
            log.info(
                "\t#{} : {}".format(
                    job_num,
                    " ".join(
                        hydra.plugins.common.utils.filter_overrides(sweep_override)
                    ),
                )
            )
            job = executor.submit(
                self.launch_job,
                sweep_override,
                "hydra.sweep.dir",
                job_num,
                hydra.plugins.common.utils.Singleton.get_state(),
            )
            jobs.append(job)

        return [j.results()[0] for j in jobs]
