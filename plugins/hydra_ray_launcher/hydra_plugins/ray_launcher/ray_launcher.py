# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import functools

from omegaconf import open_dict
from omegaconf import OmegaConf
from omegaconf import DictConfig

from hydra._internal.config_search_path import ConfigSearchPath
from hydra._internal.pathlib import Path
from hydra.plugins import Launcher
from hydra.plugins import SearchPathPlugin
from hydra.plugins.common.utils import (
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
    HydraConfig,
)

import ray

log = logging.getLogger(__name__)

def get_key(cfg, key):
    if key == '':
        return cfg
    else:
        keys = key.split('.')
        if keys[0] in cfg:
            return get_key(getattr(cfg, keys[0]), '.'.join(keys[1:]))
        else:
            return False

def merge_kwargs(kwargs1, kwargs2):
    k1 = kwargs1 if isinstance(kwargs1, DictConfig) else OmegaConf.create(kwargs1)
    k2 = kwargs2 if isinstance(kwargs2, DictConfig) else OmegaConf.create(kwargs2)
    merged = OmegaConf.merge(k1,k2)
    return merged.to_container(resolve=True)

def pass_conf(f, cfg, key):
    item = get_key(cfg, key)
    if item:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **merge_kwargs(item, kwargs))
        return wrapper
    else:
        return f

class RayLauncherSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleLauncher plugin to be discovered
    and used once the ExampleLauncher plugin is installed
    """

    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-ray-launcher", "pkg://hydra_plugins.ray_launcher.conf"
        )

def launch(*args, **kwargs):
    setup_globals()
    run_job(*args, **kwargs)

class RayLauncher(Launcher):
    def __init__(self):
        self.config = None
        self.config_loader = None
        self.task_function = None

    def setup(self, config, config_loader, task_function):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function
        
        if not ray.is_initialized(): pass_conf(ray.init, config, 'ray.init')()

    def launch(self, job_overrides):
        """
        :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
        :return: an array of return values from run_job with indexes corresponding to the input list indexes.
        """
        configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        sweep_dir = Path(str(self.config.hydra.sweep.dir))
        sweep_dir.mkdir(parents=True, exist_ok=True)
        log.info(
            "Ray Launcher is launching {} jobs locally".format(
                len(job_overrides)
            )
        )
        log.info("Sweep output dir : {}".format(sweep_dir))
        runs = []

        for idx, overrides in enumerate(job_overrides):
            log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(overrides))))
            sweep_config = self.config_loader.load_sweep_config(
                self.config, list(overrides)
            )
            with open_dict(sweep_config):
                # This typically coming from the underlying scheduler (SLURM_JOB_ID for instance)
                # In that case, it will not be available here because we are still in the main process.
                # but instead should be populated remotely before calling the task_function.
                sweep_config.hydra.job.id = idx
                sweep_config.hydra.job.num = idx
            HydraConfig().set_config(sweep_config)

            ray_remote_cfg = get_key(self.config, 'ray.remote')
            if ray_remote_cfg:
                run_job_ray = ray.remote(**ray_remote_cfg)(launch)
            else:
                run_job_ray = ray.remote(launch)

            ret = run_job_ray.remote(
                config=sweep_config,
                task_function=self.task_function,
                job_dir_key="hydra.sweep.dir",
                job_subdir_key="hydra.sweep.subdir",
            )

            runs.append(ret)
            configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        
        return [ray.get(run) for run in runs]