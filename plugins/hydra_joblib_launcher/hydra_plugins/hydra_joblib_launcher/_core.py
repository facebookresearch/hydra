# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from pathlib import Path
from typing import Any, Dict, List, Sequence

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
from joblib import Parallel, delayed  # type: ignore
from omegaconf import DictConfig, open_dict

from .joblib_launcher import JoblibLauncher

log = logging.getLogger(__name__)


def execute_job(
    idx: int,
    overrides: Sequence[str],
    config_loader: ConfigLoader,
    config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
) -> JobReturn:
    """Calls `run_job` in parallel"""
    setup_globals()
    Singleton.set_state(singleton_state)

    sweep_config = config_loader.load_sweep_config(config, list(overrides))
    with open_dict(sweep_config):
        sweep_config.hydra.job.id = "{}_{}".format(sweep_config.hydra.job.name, idx)
        sweep_config.hydra.job.num = idx
    HydraConfig.instance().set_config(sweep_config)

    ret = run_job(
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
    assert launcher.config_loader is not None
    assert launcher.task_function is not None

    configure_log(launcher.config.hydra.hydra_logging, launcher.config.hydra.verbose)
    sweep_dir = Path(str(launcher.config.hydra.sweep.dir))
    sweep_dir.mkdir(parents=True, exist_ok=True)

    # Joblib's backend is hard-coded to loky since the threading
    # backend is incompatible with Hydra
    joblib_cfg = launcher.joblib
    joblib_cfg["backend"] = "loky"
    process_joblib_cfg(joblib_cfg)

    log.info(
        "Joblib.Parallel({}) is launching {} jobs".format(
            ",".join([f"{k}={v}" for k, v in joblib_cfg.items()]),
            len(job_overrides),
        )
    )
    log.info("Launching jobs, sweep output dir : {}".format(sweep_dir))
    for idx, overrides in enumerate(job_overrides):
        log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(overrides))))

    singleton_state = Singleton.get_state()

    runs = Parallel(**joblib_cfg)(
        delayed(execute_job)(
            initial_job_idx + idx,
            overrides,
            launcher.config_loader,
            launcher.config,
            launcher.task_function,
            singleton_state,
        )
        for idx, overrides in enumerate(job_overrides)
    )

    assert isinstance(runs, List)
    for run in runs:
        assert isinstance(run, JobReturn)
    return runs
