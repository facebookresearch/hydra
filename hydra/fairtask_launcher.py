import asyncio

from fairtask import TaskQueues, gatherl

from hydra import utils
from .launcher import Launcher
import os


class FAIRTaskLauncher(Launcher):
    def __init__(self, cfg_dir, task):
        self.task = task
        self.hydra_cfg = utils.create_hydra_cfg(cfg_dir)

    def launch_job(self, sweep_instance, workdir):
        utils.setup_globals()
        utils.run_job(hydra_cfg=self.hydra_cfg,
                      task=self.task,
                      overrides=sweep_instance,
                      verbose=False, workdir=workdir)

    async def run_sweep(self, queue, sweep_configs):
        queue_name = self.hydra_cfg.hydra.launcher.queue
        print("Launching {} jobs to {} queue".format(len(sweep_configs), queue_name))
        queue = queue.task(queue_name)
        runs = []
        for i in range(len(sweep_configs)):
            sweep_override = list(sweep_configs[i])
            workdir = os.path.join(self.hydra_cfg.hydra.sweep_dir, str(i))
            print("\tWorkdir {} : {} {}".format(workdir, self.task, " ".join(sweep_override)))
            runs.append(queue(self.launch_job)(sweep_override, workdir))
        return await gatherl(runs)

    @staticmethod
    def create_queue(cfg, num_jobs):
        assert num_jobs > 0
        cfg.concurrent = num_jobs
        queues = {}
        for k, v in cfg.queues.items():
            queues[k] = utils.instantiate(v)

        # if no_workers == True, then turn off all queue functionality
        # and run everything synchronously (good for debugging)
        no_workers = False if cfg.no_workers is None else cfg.no_workers
        return TaskQueues(queues, no_workers=no_workers)

    def launch(self, sweep_configs):
        # TODO: use logger
        print("Sweep output dir : {}".format(self.hydra_cfg.hydra.sweep_dir))
        loop = asyncio.get_event_loop()
        queue = self.create_queue(self.hydra_cfg.hydra.launcher, len(sweep_configs))
        loop.run_until_complete(self.run_sweep(queue, sweep_configs))
