# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os

import submitit

import hydra._internal.utils
import hydra.plugins.common.utils
from hydra.plugins import Launcher

# pylint: disable=C0103
log = logging.getLogger(__name__)


class SubmititLauncher(Launcher):
    def __init__(self, queue, folder, queue_parameters):
        self.queue = queue
        self.queue_parameters = queue_parameters
        self.folder = folder
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

    def launch_job(self, sweep_overrides, job_dir_key, job_num):
        # stdout logging until we get the file logging going.
        # logs will be in slurm job log files
        hydra.plugins.common.utils.configure_log(None, self.verbose)
        hydra.plugins.common.utils.JobRuntime().set("num", job_num)
        if "SLURM_JOB_ID" in os.environ:
            hydra.plugins.common.utils.JobRuntime().set("id", "${env:SLURM_JOB_ID}")
        elif "CHRONOS_JOB_ID" in os.environ:
            hydra.plugins.common.utils.JobRuntime().set("id", "${env:CHRONOS_JOB_ID}")
        else:
            hydra.plugins.common.utils.JobRuntime().set("id", "unknown")
        hydra.plugins.common.utils.setup_globals()
        sweep_config = self.config_loader.load_sweep_config(
            self.config, sweep_overrides
        )

        # Populate new job variables
        sweep_config.hydra.job.id = (
            "${env:SLURM_JOB_ID}"
            if "SLURM_JOB_ID" in os.environ
            else "_UNKNOWN_SLURM_ID_"
        )
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
        num_jobs = len(job_overrides)
        assert num_jobs > 0
        self.config.hydra.job.num_jobs = num_jobs

        if self.queue == "auto":
            executor = submitit.AutoExecutor(folder=self.folder)
        elif self.queue == "slurm":
            executor = submitit.SlurmExecutor(folder=self.folder)
        elif self.queue == "chronos":
            executor = submitit.ChronosExecutor(folder=self.folder)
        elif self.queue == "local":
            executor = submitit.LocalExecutor(folder=self.folder)
        else:
            raise RuntimeError("Unsupported queue type {}".format(self.queue))

        executor.update_parameters(**self.queue_parameters[self.queue])

        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))
        os.makedirs(str(self.config.hydra.sweep.dir), exist_ok=True)
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
                self.launch_job, sweep_override, "hydra.sweep.dir", job_num
            )
            jobs.append(job)

        return [j.results() for j in jobs]
