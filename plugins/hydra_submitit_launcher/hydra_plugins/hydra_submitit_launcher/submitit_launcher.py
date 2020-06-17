# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import dataclasses
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from hydra import TaskFunction
from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.singleton import Singleton
from hydra.core.utils import (
    JobReturn,
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
)
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from omegaconf import DictConfig, OmegaConf, open_dict

from .config import BaseParams, LocalParams, SlurmParams

log = logging.getLogger(__name__)


class SubmititLauncherSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        search_path.append(
            "hydra-submitit-launcher",
            "pkg://hydra_plugins.hydra_submitit_launcher.conf",
        )


class SubmititLauncher(Launcher):
    def __init__(self, **params: Any) -> None:
        self.params = OmegaConf.structured(
            LocalParams if params["executor"].value == "local" else SlurmParams
        )
        for key, val in params.items():
            OmegaConf.update(self.params, key, val if key != "executor" else val.value)
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None
        self.sweep_configs: Optional[TaskFunction] = None

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function

    def __call__(
        self,
        sweep_overrides: List[str],
        job_dir_key: str,
        job_num: int,
        job_id: str,
        singleton_state: Dict[type, "Singleton"],
    ):
        Singleton.set_state(singleton_state)
        configure_log(self.config.hydra.job_logging, self.config.hydra.verbose)
        setup_globals()
        sweep_config = self.config_loader.load_sweep_config(
            self.config, sweep_overrides
        )
        # lazy import to ensure plugin discovery remains fast
        import submitit

        with open_dict(sweep_config.hydra.job) as job:
            # Populate new job variables
            job.id = submitit.JobEnvironment().job_id
            sweep_config.hydra.job.num = job_num

        return run_job(
            config=sweep_config,
            task_function=self.task_function,
            job_dir_key=job_dir_key,
            job_subdir_key="hydra.sweep.subdir",
        )

    def checkpoint(self, *args, **kwargs):
        """Resubmit the current callable at its current state with the same initial arguments."""
        # lazy import to ensure plugin discovery remains fast
        import submitit

        return submitit.helpers.DelayedSubmission(self, *args, **kwargs)

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        # lazy import to ensure plugin discovery remains fast
        import submitit

        num_jobs = len(job_overrides)
        assert num_jobs > 0
        exec_name = self.params.executor.value
        params = self.params

        # build executor
        init_renamer = dict(executor="cluster", submitit_folder="folder")
        init_params = {name: params[k] for k, name in init_renamer.items()}
        init_params = {
            k: v.value if isinstance(v, Enum) else v for k, v in init_params.items()
        }
        specific_init_keys = {"max_num_timeout"}
        init_params.update(
            **{
                f"{exec_name}_{x}": y
                for x, y in params.items()
                if x in specific_init_keys
            }
        )
        init_keys = specific_init_keys | set(init_renamer)  # used config keys
        executor = submitit.AutoExecutor(**init_params)

        # specify resources/parameters
        baseparams = set(dataclasses.asdict(BaseParams()).keys())
        params = {
            x if x in baseparams else f"{exec_name}_{x}": y
            for x, y in params.items()
            if x not in init_keys
        }
        executor.update_parameters(**params)

        log.info(
            f"Submitit '{exec_name}' sweep output dir : "
            f"{self.config.hydra.sweep.dir}"
        )
        sweep_dir = Path(str(self.config.hydra.sweep.dir))
        sweep_dir.mkdir(parents=True, exist_ok=True)
        if "mode" in self.config.hydra.sweep:
            mode = int(str(self.config.hydra.sweep.mode), 8)
            os.chmod(sweep_dir, mode=mode)

        params = []

        for idx, overrides in enumerate(job_overrides):
            idx = initial_job_idx + idx
            lst = " ".join(filter_overrides(overrides))
            log.info(f"\t#{idx} : {lst}")
            params.append(
                (
                    list(overrides),
                    "hydra.sweep.dir",
                    idx,
                    f"job_id_for_{idx}",
                    Singleton.get_state(),
                )
            )

        jobs = executor.map_array(self, *zip(*params))
        return [j.results()[0] for j in jobs]
