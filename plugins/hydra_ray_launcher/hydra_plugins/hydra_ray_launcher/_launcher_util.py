# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from contextlib import contextmanager
from typing import Any, Dict, Generator

import ray
from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, run_job, setup_globals
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig

# mypy complains about "unused type: ignore comment" on macos
# workaround adapted from: https://github.com/twisted/twisted/pull/1416
try:
    import importlib

    sdk = importlib.import_module("ray.autoscaler.sdk")
except ModuleNotFoundError as e:
    raise ImportError(e)

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
    hydra_context: HydraContext,
    sweep_config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
) -> JobReturn:
    setup_globals()
    Singleton.set_state(singleton_state)
    HydraConfig.instance().set_config(sweep_config)
    return run_job(
        hydra_context=hydra_context,
        task_function=task_function,
        config=sweep_config,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )


def launch_job_on_ray(
    hydra_context: HydraContext,
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
        hydra_context=hydra_context,
        sweep_config=sweep_config,
        task_function=task_function,
        singleton_state=singleton_state,
    )
    return ret


@contextmanager
def ray_tmp_dir(config: Dict[Any, Any], run_env: str) -> Generator[Any, None, None]:
    out = sdk.run_on_cluster(  # type: ignore[attr-defined]
        config, run_env=run_env, cmd="echo $(mktemp -d)", with_output=True
    ).decode()

    tmppath = [
        x
        for x in out.strip().split()
        if x.startswith("/tmp/") and "ray-config" not in x  # nosec
    ]
    assert len(tmppath) == 1, f"tmppath is : {tmppath}"
    tmp_path = tmppath[0]
    log.info(f"Created temp path on remote server {tmp_path}")
    yield tmp_path
    sdk.run_on_cluster(config, run_env=run_env, cmd=f"rm -rf {tmp_path}")  # type: ignore[attr-defined]
