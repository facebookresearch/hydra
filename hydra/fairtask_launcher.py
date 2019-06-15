import asyncio
import os

from fairtask import TaskQueues, gatherl
from omegaconf import OmegaConf

from hydra import utils
from .launcher import Launcher



class FAIRTaskLauncher(Launcher):
    def __init__(self, conf_dir):
        self.cfg = OmegaConf.from_filename(os.path.join(conf_dir, "fairtask.yaml"))

    async def get_runs(self, sweep_configs):
        gatherl
        pass

    def create_queue(self, cfg, num_jobs):
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
        for s in sweep_configs:
            print(s)

        queue = self.create_queue(self.cfg.launcher, len(s))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_runs())
    #
    # def launch_jobs(self, cfg,, queue, sweep_config):
    #     log.info(f"Launching {len(sweep_config)} jobs")
    #     if sweep_config is not None:
    #         os.makedirs(log_dir, exist_ok=True)
    #         with open(os.path.join(log_dir, 'sweep-config.yaml'), 'w') as file:
    #             file.write(sweep_config.pretty())
    #
    #     overrides = []
    #     for instance in range(cfg.launcher.instances):
    #         override = OmegaConf.empty()
    #         instance_id = f"{instance}"
    #         override.instance_id = instance_id
    #         override.log_dir = log_dir
    #         override.random_seed = cfg.launcher.random_seed + instance
    #         override.log_dir_suffix = instance_id
    #         override.log_config = cfg.launcher.log.config
    #
    #         if sweep_config is not None:
    #             override.merge_from(sweep_config)
    #
    #         # Put user provided parameters into spec for easy access (used for visualizing etc)
    #         override_list = list(filter(lambda s: not s.startswith("launcher."), args.overrides))
    #         override.spec = OmegaConf.merge(sweep_config or OmegaConf.empty(), OmegaConf.from_cli(override_list))
    #         if args.presets is not None:
    #             for p in args.presets.split(','):
    #                 p = p.split('=')
    #                 override.spec.presets[p[0]] = p[1]
    #
    #         overrides.append(override)
    #
    #     return [queue.task(cfg.launcher.queue)(launch)(sys.argv, cfg.target, override) for override in overrides]
    #
