# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import asyncio
import logging
import os

from omegaconf import open_dict

import hydra.plugins.common.utils
from hydra import utils
from hydra.plugins import Launcher

# TODO: initialize logger before importing fairtask until comments at
# https://github.com/fairinternal/fairtask/pull/23 are addressed
log = logging.getLogger(__name__)  # noqa: E402

from fairtask import TaskQueues, gatherl


class FAIRTaskLauncher(Launcher):
    def __init__(self, queue, queues, no_workers=False):
        self.queue_name = queue
        self.queues = queues
        self.config = None
        self.task_function = None
        self.verbose = None
        self.sweep_configs = None
        self.no_workers = no_workers
        self.config_loader = None

    def setup(self, config, config_loader, task_function, verbose):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function
        self.verbose = verbose

    def launch_job(self, sweep_overrides, job_dir_key, job_num):
        # stdout logging until we get the file logging going, logs will be in slurm job log files
        hydra.plugins.common.utils.configure_log(None, self.verbose)
        hydra.plugins.common.utils.setup_globals()
        sweep_config = self.config_loader.load_sweep_config(
            self.config, sweep_overrides
        )

        with open_dict(sweep_config):
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

    async def run_sweep(self, queue, job_overrides):
        log.info(
            "Launching {} jobs to {} queue".format(len(job_overrides), self.queue_name)
        )
        num_jobs = len(job_overrides)
        queue = queue.task(self.queue_name)
        runs = []
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
            runs.append(
                queue(self.launch_job)(sweep_override, "hydra.sweep.dir", job_num)
            )

        return await gatherl(runs)

    def create_queue(self, num_jobs):
        assert num_jobs > 0
        # num_jobs is needed to instantiate the queue below
        with open_dict(self.config):
            self.config.hydra.job.num_jobs = num_jobs
        queues = {}
        for queue_name, queue_conf in self.queues.items():
            queues[queue_name] = utils.instantiate(queue_conf)

        # if no_workers == True, then turn off all queue functionality
        # and run everything synchronously (good for debugging)
        return TaskQueues(queues, no_workers=self.no_workers)

    def launch(self, job_overrides):
        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))
        os.makedirs(str(self.config.hydra.sweep.dir), exist_ok=True)
        loop = asyncio.get_event_loop()
        with self.create_queue(num_jobs=len(job_overrides)) as queue:
            return loop.run_until_complete(self.run_sweep(queue, job_overrides))
