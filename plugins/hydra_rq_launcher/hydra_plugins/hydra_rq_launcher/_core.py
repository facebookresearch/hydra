# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Sequence

import cloudpickle
from fakeredis import FakeStrictRedis
from hydra.core.config_loader import ConfigLoader
from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import (
    JobReturn,
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
)
from hydra.types import TaskFunction
from omegaconf import DictConfig, OmegaConf, open_dict
from redis import Redis
from rq import Queue

from .rq_launcher import RQLauncher

log = logging.getLogger(__name__)


def execute_job(
    idx: int,
    overrides: Sequence[str],
    config_loader: ConfigLoader,
    config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
    redis_job_id: str,
) -> JobReturn:
    setup_globals()
    Singleton.set_state(singleton_state)

    sweep_config = config_loader.load_sweep_config(config, list(overrides))
    with open_dict(sweep_config):
        sweep_config.hydra.job.id = redis_job_id
        sweep_config.hydra.job.num = idx
    HydraConfig.instance().set_config(sweep_config)

    ret = run_job(
        config=sweep_config,
        task_function=task_function,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )

    return ret


def launch(
    launcher: RQLauncher, job_overrides: Sequence[Sequence[str]], initial_job_idx: int,
) -> JobReturn:
    """
    :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
    :param initial_job_idx: Initial job idx in batch.
    :return: an array of return values from run_job with indexes corresponding to the input list indexes.
    """
    setup_globals()
    assert launcher.config is not None
    assert launcher.config_loader is not None
    assert launcher.task_function is not None

    configure_log(launcher.config.hydra.hydra_logging, launcher.config.hydra.verbose)
    sweep_dir = Path(str(launcher.config.hydra.sweep.dir))
    sweep_dir.mkdir(parents=True, exist_ok=True)

    # RQ configuration
    rq_cfg = launcher.rq

    # Redis configuration
    is_async = not rq_cfg.redis.mock
    if is_async:
        connection = Redis(
            host=rq_cfg.redis.host,
            port=rq_cfg.redis.port,
            db=rq_cfg.redis.db,
            password=rq_cfg.redis.password,
        )
    else:
        log.info("Running in synchronous mode")
        connection = FakeStrictRedis()
    queue = Queue(
        name=rq_cfg.queue,
        connection=connection,
        is_async=is_async,
        serializer=cloudpickle,
    )

    # Enqueue jobs
    jobs = []
    singleton_state = Singleton.get_state()
    log.info(
        f"RQ Launcher is enqueuing {len(job_overrides)} job(s) in queue : {rq_cfg.queue}"
    )
    log.info("Sweep output dir : {}".format(sweep_dir))
    if not sweep_dir.is_absolute():
        log.warn(
            "Using relative sweep dir: Please be aware that dir will be relative to where workers are started from."
        )

    for idx, overrides in enumerate(job_overrides):
        description = " ".join(filter_overrides(overrides))

        enqueue_keywords = OmegaConf.to_container(rq_cfg.enqueue, resolve=True)
        if enqueue_keywords["job_id"] is None:
            enqueue_keywords["job_id"] = str(uuid.uuid4())
        if enqueue_keywords["description"] is None:
            enqueue_keywords["description"] = description

        job = queue.enqueue(
            execute_job,
            idx=initial_job_idx + idx,
            overrides=overrides,
            config_loader=launcher.config_loader,
            config=launcher.config,
            task_function=launcher.task_function,
            singleton_state=singleton_state,
            redis_job_id=enqueue_keywords["job_id"],
            **enqueue_keywords,
        )
        jobs.append(job)

        log.info(f"Enqueued {job.get_id()}")
        log.info(f"\t#{idx+1} : {description}")

    log.info("Finished enqueuing")
    if rq_cfg.stop_after_enqueue:
        raise StopAfterEnqueue

    log.info(f"Polling job statuses every {rq_cfg.wait_polling} sec")
    while True:
        job_ids_done = [
            job.get_id() for job in jobs if job.get_status() in ["finished", "failed"]
        ]
        if len(job_ids_done) == len(jobs):
            break
        else:
            time.sleep(rq_cfg.wait_polling)

    runs = []
    for job in jobs:
        result = job.result if job.result is not None else None
        runs.append(result)

    assert isinstance(runs, List)
    for run in runs:
        assert isinstance(run, JobReturn)

    return runs


class StopAfterEnqueue(Exception):
    pass
