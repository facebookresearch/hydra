# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from pathlib import Path
from typing import Any, Dict, Union, List, Sequence
from itertools import repeat
from concurrent.futures import wait, FIRST_COMPLETED, ALL_COMPLETED

from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import (
    JobReturn,
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
)
from hydra.plugins.experiment_sequence import ExperimentSequence
from hydra.types import HydraContext, TaskFunction
from loky import get_reusable_executor
from omegaconf import DictConfig, open_dict
import multiprocessing as mp

from .loky_launcher import LokyLauncher

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
        sweep_config.hydra.job.id = "{}_{}".format(sweep_config.hydra.job.name, idx)
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


def process_loky_cfg(loky_cfg: Dict[str, Any]) -> None:
    for k in ["timeout", "max_workers"]:
        if k in loky_cfg.keys():
            try:
                val = loky_cfg.get(k)
                if val:
                    loky_cfg[k] = int(val)
            except ValueError:
                pass


def launch(
    launcher: LokyLauncher,
    job_overrides: Union[Sequence[Sequence[str]], ExperimentSequence],
    initial_job_idx: int,
) -> Sequence[JobReturn]:
    """
    :param job_overrides: an Iterable of List<String>, where each inner list is the arguments for one job run.
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

    loky_cfg = launcher.loky
    process_loky_cfg(loky_cfg)
    singleton_state = Singleton.get_state()

    worker_pool = get_reusable_executor(**loky_cfg)
    batch_size = v if (v := loky_cfg['max_workers']) is not None else mp.cpu_count()

    runs = [None for _ in range(len(job_overrides))]
    log.info(
        "ReusableExectutor({}) is launching {} jobs".format(
            ",".join([f"{k}={v}" for k, v in loky_cfg.items()]),
            'generator of' if isinstance(job_overrides, ExperimentSequence) else len(job_overrides),
        )
    )
    running_tasks = {}
    for idx, override in enumerate(job_overrides):
        log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(override))))
        running_tasks[worker_pool.submit(
            execute_job,
            initial_job_idx + idx,
            override,
            launcher.hydra_context,
            launcher.config,
            launcher.task_function,
            singleton_state
        )] = (override, idx)

        if len(running_tasks) == batch_size:
            finished, non_finished = wait(running_tasks, return_when=FIRST_COMPLETED)
            overrides = [running_tasks[f] for f in finished]
            results = [f.result() for f in finished]
            running_tasks = {task: running_tasks[task] for task in non_finished}
            for (_, idx), res in zip(overrides, results):
                runs[idx] = res
            if isinstance(job_overrides, ExperimentSequence):
                for experiment_result in zip(overrides, results):
                    job_overrides.update_sequence(experiment_result)
    
    finished, _ = wait(running_tasks, return_when=ALL_COMPLETED)
    overrides = [running_tasks[f] for f in finished]
    results = [f.result() for f in finished]

    for (_, idx), res in zip(overrides, results):
        runs[idx] = res
    if isinstance(job_overrides, ExperimentSequence):
        for experiment_result in zip(overrides, results):
                job_overrides.update_sequence(experiment_result)
    
    assert isinstance(runs, List)
    for run in runs:
        assert isinstance(run, JobReturn)
    return runs
