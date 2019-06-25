import asyncio
import os

import itertools
from fairtask import TaskQueues, gatherl

from hydra import utils
from .launcher import Launcher


class FAIRTaskLauncher(Launcher):
    def __init__(self, cfg_dir, cfg_filename, hydra_cfg, task_function, overrides):
        self.cfg_dir = cfg_dir
        self.cfg_filename = cfg_filename
        self.hydra_cfg = hydra_cfg
        self.task_function = task_function
        self.sweep_configs = FAIRTaskLauncher.get_sweep(overrides)

    def launch_job(self, sweep_overrides, workdir):
        utils.setup_globals()
        utils.run_job(self.cfg_dir,
                      self.cfg_filename,
                      hydra_cfg=self.hydra_cfg,
                      task_function=self.task_function,
                      overrides=sweep_overrides,
                      verbose=False,
                      workdir=workdir)

    async def run_sweep(self, queue, sweep_configs):
        queue_name = self.hydra_cfg.hydra.launcher.queue
        print("Launching {} jobs to {} queue".format(len(sweep_configs), queue_name))
        queue = queue.task(queue_name)
        runs = []
        for i in range(len(sweep_configs)):
            sweep_override = list(sweep_configs[i])
            workdir = os.path.join(self.hydra_cfg.hydra.sweep_dir, str(i))
            print("\tWorkdir {} : {}".format(workdir, " ".join(sweep_override)))
            runs.append(queue(self.launch_job)(sweep_override, workdir))
        return await gatherl(runs)

    @staticmethod
    def create_queue(cfg, num_jobs):
        assert num_jobs > 0
        cfg.launcher.concurrent = num_jobs
        queues = {}
        for queue_name, queue_conf in cfg.launcher.queues.items():
            queues[queue_name] = utils.instantiate(queue_conf)

        # if no_workers == True, then turn off all queue functionality
        # and run everything synchronously (good for debugging)
        no_workers = False if cfg.no_workers is None else cfg.no_workers
        return TaskQueues(queues, no_workers=no_workers)

    @staticmethod
    def get_sweep(overrides):
        lists = []
        for s in overrides:
            key, value = s.split('=')
            lists.append(["{}={}".format(key, value) for value in value.split(',')])

        return list(itertools.product(*lists))

    def launch(self):
        # TODO: use logger
        print("Sweep output dir : {}".format(self.hydra_cfg.hydra.sweep_dir))
        os.makedirs(self.hydra_cfg.hydra.sweep_dir, exist_ok=True)
        self.hydra_cfg.hydra.job_cwd = self.hydra_cfg.hydra.sweep_dir
        loop = asyncio.get_event_loop()
        queue = self.create_queue(self.hydra_cfg.hydra, len(self.sweep_configs))
        loop.run_until_complete(self.run_sweep(queue, self.sweep_configs))

        return self.sweep_configs
