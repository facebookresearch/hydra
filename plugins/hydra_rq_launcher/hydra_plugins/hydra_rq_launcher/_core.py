# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Sequence

import cloudpickle  # type: ignore
from fakeredis import FakeStrictRedis  # type: ignore
from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import (
    JobReturn,
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
)
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig, OmegaConf, open_dict
from redis import Redis
from rq import Queue  # type: ignore

from .rq_launcher import RQLauncher

log = logging.getLogger(__name__)


def execute_job(
    hydra_context: HydraContext,
    sweep_config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
) -> JobReturn:
    setup_globals()
    Singleton.set_state(singleton_state)

    HydraConfig.instance().set_config(sweep_config)

    ret = run_job(
        hydra_context=hydra_context,
        task_function=task_function,
        config=sweep_config,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )

    return ret


def launch(
    launcher: RQLauncher, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
) -> Sequence[JobReturn]:
    """
    :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
    :param initial_job_idx: Initial job idx in batch.
    :return: an array of return values from run_job with indexes corresponding to the input list indexes.
    """
    setup_globals()
    assert launcher.config is not None
    assert launcher.task_function is not None
    assert launcher.hydra_context is not None

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
            ssl=rq_cfg.redis.ssl,
            ssl_ca_certs=rq_cfg.redis.ssl_ca_certs,
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
    jobs: List[Any] = []
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
        assert isinstance(enqueue_keywords, dict)
        if enqueue_keywords["job_timeout"] is None:
            enqueue_keywords["job_timeout"] = -1
        if enqueue_keywords["result_ttl"] is None:
            enqueue_keywords["result_ttl"] = -1
        if enqueue_keywords["failure_ttl"] is None:
            enqueue_keywords["failure_ttl"] = -1
        if enqueue_keywords["job_id"] is None:
            enqueue_keywords["job_id"] = str(uuid.uuid4())
        if enqueue_keywords["description"] is None:
            enqueue_keywords["description"] = description

        sweep_config = launcher.hydra_context.config_loader.load_sweep_config(
            launcher.config, list(overrides)
        )
        with open_dict(sweep_config):
            sweep_config.hydra.job.id = enqueue_keywords["job_id"]
            sweep_config.hydra.job.num = initial_job_idx + idx

        job = queue.enqueue(
            execute_job,
            hydra_context=launcher.hydra_context,
            sweep_config=sweep_config,
            task_function=launcher.task_function,
            singleton_state=singleton_state,
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

    runs: List[JobReturn] = []
    for job in jobs:
        result = job.result if job.result is not None else None
        runs.append(result)

    return runs


class StopAfterEnqueue(Exception):
    pass
