# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Sequence

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

log = logging.getLogger(__name__)


class SubmititLauncherSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        search_path.append(
            "hydra-submitit-launcher",
            "pkg://hydra_plugins.hydra_submitit_launcher.conf",
        )


class SubmititLauncher(Launcher):
    def __init__(self, executor: str, folder: str, params: DictConfig) -> None:
        self.executor = executor
        self.params = params
        self.folder = folder
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

        # make sure you don't change inplace
        queue_parameters = self.params.copy()
        OmegaConf.set_struct(queue_parameters, True)
        init_parameters = {"max_num_timeout"}
        executor = submitit.AutoExecutor(
            folder=self.folder,
            cluster=self.executor.value,
            **{
                f"{self.executor.value}_{x}": y
                for x, y in queue_parameters.items()
                if x in init_parameters
            },
        )
        executor.update_parameters(
            **{
                # f"{self.executor.value}_{x}": y
                x: y
                for x, y in queue_parameters.items()
                if x not in init_parameters
            }
        )

        log.info(
            "Submitit '{}' sweep output dir : {}".format(
                self.executor, self.config.hydra.sweep.dir
            )
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
