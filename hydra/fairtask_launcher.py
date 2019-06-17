import asyncio
import os

from fairtask import TaskQueues, gatherl

from hydra import utils
from omegaconf import OmegaConf
from .launcher import Launcher
from .task import Task


class FAIRTaskLauncher(Launcher):
    def __init__(self, conf_dir, task):
        self.task = task
        self.cfg = OmegaConf.load(os.path.join(conf_dir, "fairtask.yaml"))

    def launch_job(self, sweep_instance):
        cfg_dir = utils.find_cfg_dir(self.task)
        task_cfg = utils.create_task_cfg(cfg_dir, self.task, sweep_instance)
        cfg = task_cfg['cfg']
        6# TODO: control verbose
        utils.configure_log(cfg_dir, cfg, verbose=False)
        task = utils.create_task(self.task)
        assert isinstance(task, Task)
        task.setup(cfg)
        task.run(cfg)

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
