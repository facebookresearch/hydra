import os

import submitit

from hydra import utils
from .launcher import Launcher


class SubmititLauncher(Launcher):

    def __init__(self, queue, folder):
        self.queue = queue
        self.folder = folder
        self.cfg_dir = None
        self.cfg_filename = None
        self.hydra_cfg = None
        self.task_function = None
        self.verbose = None
        self.sweep_configs = None

    def setup(self, cfg_dir, cfg_filename, hydra_cfg, task_function, verbose, overrides):
        self.cfg_dir = cfg_dir
        self.cfg_filename = cfg_filename
        self.hydra_cfg = hydra_cfg
        self.task_function = task_function
        self.verbose = verbose
        self.sweep_configs = utils.get_sweep(overrides)

    def launch_job(self, sweep_overrides, workdir, job_num, job_name):
        # stdout logging until we get the file logging going.
        # logs will be in slurm job log files
        utils.configure_log(None, self.verbose)
        utils.JobRuntime().set('num', job_num)
        utils.JobRuntime().set('name', job_name)
        if 'SLURM_JOB_ID' in os.environ:
            utils.JobRuntime().set('id', '${env:SLURM_JOB_ID}')
        else:
            utils.JobRuntime().set('id', 'unknown')
        utils.setup_globals()

        return utils.run_job(self.cfg_dir,
                             self.cfg_filename,
                             hydra_cfg=self.hydra_cfg,
                             task_function=self.task_function,
                             overrides=sweep_overrides,
                             verbose=self.verbose,
                             job_dir=workdir,
                             job_subdir_key='hydra.sweep.subdir')

    def launch(self):
        if self.queue == 'slurm':
            executor = submitit.SlurmExecutor(folder=self.folder)
        elif self.queue == 'chronos':
            executor = submitit.ChronosExecutor(folder=self.folder)
        elif self.queue == 'local':
            executor = submitit.LocalExecutor(folder=self.folder)
        else:
            raise RuntimeError('Unsupported queue type {}'.format(self.queue))

        # TODO: use logger
        print("Sweep output dir : {}".format(self.hydra_cfg.hydra.sweep.dir))
        os.makedirs(self.hydra_cfg.hydra.sweep.dir, exist_ok=True)
        jobs = []
        for job_num in range(len(self.sweep_configs)):
            sweep_override = list(self.sweep_configs[job_num])
            print("\t#{} : {}".format(job_num, " ".join(sweep_override)))
            job = executor.submit(self.launch_job,
                                  sweep_override,
                                  self.hydra_cfg.hydra.sweep.dir,
                                  job_num,
                                  utils.JobRuntime().get('name'))
            jobs.append(job)

        outputs = [job.result() for job in jobs]

