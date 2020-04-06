# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
import logging
import os
import sys
from typing import Sequence

import cloudpickle
import ray
from omegaconf import DictConfig, open_dict, OmegaConf

from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import (
    JobReturn,
    run_job,
    setup_globals,
)

log = logging.getLogger(__name__)


def launch_jobs(temp_dir: str) -> Sequence[JobReturn]:

    setup_globals()
    runs = []
    for d in os.listdir(temp_dir):
        job_idx = d
        with open(os.path.join(temp_dir, job_idx, "params.pkl"), "rb") as f:
            params = cloudpickle.load(f)

            idx = params["idx"]
            overrides = params["overrides"]
            config = params["config"]
            config_loader = params["config_loader"]
            task_function = params["task_function"]
            singleton_state = params["singleton_state"]

            if not ray.is_initialized():
                pass_conf(ray.init, config, 'hydra.launcher.params.ray_init_config')()

            setup_globals()
            Singleton.set_state(singleton_state)

            sweep_config = config_loader.load_sweep_config(config, list(overrides))

            with open_dict(sweep_config):
                sweep_config.hydra.job.id = "{}_{}".format(
                    sweep_config.hydra.job.name, idx
                )
                sweep_config.hydra.job.num = idx
            HydraConfig.instance().set_config(sweep_config)

            ray_remote_cfg = get_key(config, 'hydra.launcher.params.ray_remote_config')
            if ray_remote_cfg:
                run_job_ray = ray.remote(**ray_remote_cfg)(launch)
            else:
                run_job_ray = ray.remote(launch)
            ret = run_job_ray.remote(
                config=sweep_config,
                task_function=task_function,
                job_dir_key="hydra.sweep.dir",  # TODO make this configurable
                job_subdir_key="hydra.sweep.subdir",
            )
            runs.append(ret)

    return [ray.get(run) for run in runs]


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
    merged = OmegaConf.merge(k1, k2)
    return OmegaConf.to_container(merged, resolve=True)


def pass_conf(f, cfg, key):
    item = get_key(cfg, key)
    if item:

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **merge_kwargs(item, kwargs))

        return wrapper
    else:
        return f


def launch(*args, **kwargs):
    setup_globals()
    run_job(*args, **kwargs)


if __name__ == "__main__":
    launch_jobs(sys.argv[1])
