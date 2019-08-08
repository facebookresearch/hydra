# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os

import submitit

from hydra import Launcher
from hydra import utils

# pylint: disable=C0103
log = logging.getLogger(__name__)


class SubmititLauncher(Launcher):

    def __init__(self, queue, folder, queue_parameters):
        self.queue = queue
        self.queue_parameters = queue_parameters
        self.folder = folder
        self.cfg_dir = None
        self.cfg_filename = None
        self.hydra_cfg = None
        self.task_function = None
        self.verbose = None
        self.config_loader = None
        self.sweep_configs = None

    def setup(self, config_loader, hydra_cfg, task_function, verbose):
        self.config_loader = config_loader
        self.hydra_cfg = hydra_cfg
        self.task_function = task_function
        self.verbose = verbose

    def launch_job(self, sweep_overrides, workdir, job_num, job_name):
        # stdout logging until we get the file logging going.
        # logs will be in slurm job log files
        utils.configure_log(None, self.verbose)
        utils.JobRuntime().set('num', job_num)
        utils.JobRuntime().set('name', job_name)
        if 'SLURM_JOB_ID' in os.environ:
            utils.JobRuntime().set('id', '${env:SLURM_JOB_ID}')
        elif 'CHRONOS_JOB_ID' in os.environ:
            utils.JobRuntime().set('id', '${env:CHRONOS_JOB_ID}')
        else:
            utils.JobRuntime().set('id', 'unknown')
        utils.setup_globals()

        return utils.run_job(config_loader=self.config_loader,
                             hydra_cfg=self.hydra_cfg,
                             task_function=self.task_function,
                             overrides=sweep_overrides,
                             verbose=self.verbose,
                             job_dir=workdir,
                             job_subdir_key='hydra.sweep.subdir')

    def launch(self, job_overrides):
        num_jobs = len(job_overrides)
        assert num_jobs > 0
        utils.HydraRuntime().set('num_jobs', num_jobs)

        if self.queue == 'auto':
            executor = submitit.AutoExecutor(folder=self.folder)
        elif self.queue == 'slurm':
            executor = submitit.SlurmExecutor(folder=self.folder)
        elif self.queue == 'chronos':
            executor = submitit.ChronosExecutor(folder=self.folder)
        elif self.queue == 'local':
            executor = submitit.LocalExecutor(folder=self.folder)
        else:
            raise RuntimeError('Unsupported queue type {}'.format(self.queue))

        executor.update_parameters(**self.queue_parameters[self.queue])

        log.info(
            "Sweep output dir : {}".format(
                self.hydra_cfg.hydra.sweep.dir))
        os.makedirs(self.hydra_cfg.hydra.sweep.dir, exist_ok=True)
        jobs = []
        for job_num in range(num_jobs):
            sweep_override = list(job_overrides[job_num])
            log.info(
                "\t#{} : {}".format(
                    job_num, " ".join(
                        utils.filter_overrides(sweep_override))))
            job = executor.submit(self.launch_job,
                                  sweep_override,
                                  self.hydra_cfg.hydra.sweep.dir,
                                  job_num,
                                  utils.JobRuntime().get('name'))
            jobs.append(job)

        return [j.results() for j in jobs]
