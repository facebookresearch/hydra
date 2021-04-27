# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
from contextlib import contextmanager
from subprocess import PIPE, Popen
from typing import Any, Dict, Generator, List, Tuple

import ray
from ray.autoscaler import sdk
from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, run_job, setup_globals
from hydra.types import TaskFunction
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)

JOB_SPEC_PICKLE = "job_spec.pkl"
JOB_RETURN_PICKLE = "returns.pkl"


def start_ray(init_cfg: DictConfig) -> None:
    if not ray.is_initialized():
        log.info(f"Initializing ray with config: {init_cfg}")
        if init_cfg:
            ray.init(**init_cfg)
        else:
            ray.init()
    else:
        log.info("Ray is already running.")


def _run_job(
    sweep_config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
) -> JobReturn:
    setup_globals()
    Singleton.set_state(singleton_state)
    HydraConfig.instance().set_config(sweep_config)
    return run_job(
        config=sweep_config,
        task_function=task_function,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )


def launch_job_on_ray(
    ray_remote: DictConfig,
    sweep_config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Any,
) -> Any:
    if ray_remote:
        run_job_ray = ray.remote(**ray_remote)(_run_job)
    else:
        run_job_ray = ray.remote(_run_job)

    ret = run_job_ray.remote(
        sweep_config=sweep_config,
        task_function=task_function,
        singleton_state=singleton_state,
    )
    return ret


@contextmanager
def ray_tmp_dir(config: Dict) -> Generator[Any, None, None]:
    out = sdk.run_on_cluster(
                config, cmd="echo $(mktemp -d)", with_output=True).decode()
    
    tmppath = [
        x
        for x in out.strip().split()
        if x.startswith("/tmp/") and "ray-config" not in x  # nosec
    ]
    assert len(tmppath) == 1, f"tmppath is : {tmppath}"
    tmp_path = tmppath[0]
    log.info(f"Created temp path on remote server {tmp_path}")
    yield tmp_path
    sdk.run_on_cluster(config, cmd=f"rm -rf {tmp_path}")
