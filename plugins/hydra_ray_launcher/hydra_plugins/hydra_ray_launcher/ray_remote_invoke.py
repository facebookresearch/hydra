# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
import logging
import os
import sys
from typing import Sequence

import cloudpickle
import ray
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
            config = params["config"]
            sweep_config = params["sweep_config"]
            task_function = params["task_function"]
            singleton_state = params["singleton_state"]

            if not ray.is_initialized():
                ray.init(config.get('hydra.launcher.params.ray_init_config'))

            setup_globals()
            Singleton.set_state(singleton_state)

            ray_remote_cfg = config.get('hydra.launcher.params.ray_remote_config')
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


def launch(*args, **kwargs):
    setup_globals()
    run_job(*args, **kwargs)


if __name__ == "__main__":
    launch_jobs(sys.argv[1])
