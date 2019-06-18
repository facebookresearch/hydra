import asyncio
import os

from fairtask import TaskQueues, gatherl

from hydra import utils
from omegaconf import OmegaConf
from .launcher import Launcher


class FAIRTaskLauncher(Launcher):
    def __init__(self, conf_dir, task):
        self.task = task
        self.cfg = OmegaConf.load(os.path.join(conf_dir, "fairtask.yaml"))

    def launch_job(self, sweep_instance):
        # TODO: control verbose
        utils.run_job(task=self.task, overrides=sweep_instance, verbose=False, working_directory='sweep')

    async def run_sweep(self, queue, sweep_configs):
        queue = queue.task(self.cfg.launcher.queue)
        runs = [queue(self.launch_job)(sweep_instance) for sweep_instance in sweep_configs]
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
        loop = asyncio.get_event_loop()
        queue = self.create_queue(self.cfg.launcher, len(sweep_configs))
        loop.run_until_complete(self.run_sweep(queue, sweep_configs))
