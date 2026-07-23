# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from pathlib import Path
from typing import Any, Dict, List, Sequence

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
from joblib import Parallel, delayed, parallel_backend  # type: ignore
from omegaconf import DictConfig, open_dict

from .joblib_launcher import JoblibLauncher

log = logging.getLogger(__name__)


def execute_job(
    idx: int,
    overrides: Sequence[str],
    hydra_context: HydraContext,
    config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
) -> JobReturn:
    """Calls `run_job` in parallel"""
    setup_globals()
    Singleton.set_state(singleton_state)

    sweep_config = hydra_context.config_loader.load_sweep_config(
        config, list(overrides)
    )
    with open_dict(sweep_config):
        sweep_config.hydra.job.id = f"{sweep_config.hydra.job.name}_{idx}"
        sweep_config.hydra.job.num = idx
    HydraConfig.instance().set_config(sweep_config)

    ret = run_job(
        hydra_context=hydra_context,
        config=sweep_config,
        task_function=task_function,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )

    return ret


def process_joblib_cfg(joblib_cfg: Dict[str, Any]) -> None:
    for k in ["pre_dispatch", "batch_size", "max_nbytes"]:
        if k in joblib_cfg.keys():
            try:
                val = joblib_cfg.get(k)
                if val:
                    joblib_cfg[k] = int(val)
            except ValueError:
                pass


def launch(
    launcher: JoblibLauncher,
    job_overrides: Sequence[Sequence[str]],
    initial_job_idx: int,
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

    # Joblib's backend is hard-coded to loky since the threading
    # backend is incompatible with Hydra
    joblib_cfg = dict(launcher.joblib)
    joblib_cfg["backend"] = "loky"
    process_joblib_cfg(joblib_cfg)
    inner_max_num_threads = joblib_cfg.pop("inner_max_num_threads", None)

    backend = None
    backend_cfg = None
    parallel_cfg = dict(joblib_cfg)
    if inner_max_num_threads is not None:
        backend = parallel_cfg.pop("backend")
        parallel_cfg.pop("prefer", None)
        parallel_cfg.pop("require", None)
        backend_cfg = {"inner_max_num_threads": inner_max_num_threads}
        if "n_jobs" in parallel_cfg:
            backend_cfg["n_jobs"] = parallel_cfg.pop("n_jobs")

    parallel_args = ",".join(f"{k}={v}" for k, v in parallel_cfg.items())
    if backend_cfg is None:
        launch_msg = f"Joblib.Parallel({parallel_args})"
    else:
        backend_args = ",".join(f"{k}={v}" for k, v in backend_cfg.items())
        launch_msg = (
            f"joblib.parallel_backend({backend},{backend_args}) "
            f"with Joblib.Parallel({parallel_args})"
        )

    log.info(
        "{} is launching {} jobs".format(
            launch_msg,
            len(job_overrides),
        ),
    )
    log.info(f"Launching jobs, sweep output dir : {sweep_dir}")
    for idx, overrides in enumerate(job_overrides):
        log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(overrides))))

    singleton_state = Singleton.get_state()

    calls = (
        delayed(execute_job)(
            initial_job_idx + idx,
            overrides,
            launcher.hydra_context,
            launcher.config,
            launcher.task_function,
            singleton_state,
        )
        for idx, overrides in enumerate(job_overrides)
    )
    if backend_cfg is None:
        runs = Parallel(**parallel_cfg)(calls)
    else:
        assert backend is not None
        with parallel_backend(backend, **backend_cfg):
            runs = Parallel(**parallel_cfg)(calls)

    assert isinstance(runs, List)
    for run in runs:
        assert isinstance(run, JobReturn)
    return runs
