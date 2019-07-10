import asyncio
import os

from fairtask import TaskQueues, gatherl

from hydra import utils
from hydra import Launcher


class FAIRTaskLauncher(Launcher):
    def __init__(self, queue, queues, no_workers=False):
        self.queue_name = queue
        self.queues = queues
        self.cfg_dir = None
        self.cfg_filename = None
        self.hydra_cfg = None
        self.task_function = None
        self.verbose = None
        self.sweep_configs = None
        self.no_workers = no_workers

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

    async def run_sweep(self, queue, sweep_configs):
        print("Launching {} jobs to {} queue".format(len(sweep_configs), self.queue_name))
        queue = queue.task(self.queue_name)
        runs = []
        for job_num in range(len(sweep_configs)):
            sweep_override = list(sweep_configs[job_num])
            print("\t#{} : {}".format(job_num, " ".join(sweep_override)))
            runs.append(queue(self.launch_job)(
                sweep_override,
                self.hydra_cfg.hydra.sweep.dir,
                job_num,
                utils.JobRuntime().get('name')))
        return await gatherl(runs)

    def create_queue(self):
        num_jobs = len(self.sweep_configs)
        assert num_jobs > 0
        self.hydra_cfg.hydra.launcher.concurrent = num_jobs
        queues = {}
        for queue_name, queue_conf in self.queues.items():
            queues[queue_name] = utils.instantiate(queue_conf)

        # if no_workers == True, then turn off all queue functionality
        # and run everything synchronously (good for debugging)
        return TaskQueues(queues, no_workers=self.no_workers)

    def launch(self):
        # TODO: use logger
        print("Sweep output dir : {}".format(self.hydra_cfg.hydra.sweep.dir))
        os.makedirs(self.hydra_cfg.hydra.sweep.dir, exist_ok=True)
        loop = asyncio.get_event_loop()
        with self.create_queue() as queue:
            return loop.run_until_complete(self.run_sweep(queue, self.sweep_configs))
