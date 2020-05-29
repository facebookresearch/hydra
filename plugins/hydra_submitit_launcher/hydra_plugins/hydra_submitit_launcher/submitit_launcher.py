# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
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


class SubmititLauncherDefaults(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        search_path.append(
            "hydra-submitit-launcher",
            "pkg://hydra_plugins.hydra_submitit_launcher.conf",
        )


class SubmititLauncher(Launcher):
    def __init__(self, queue: str, folder: str, queue_parameters: DictConfig) -> None:
        self.queue = queue
        self.queue_parameters = queue_parameters
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
        singleton_state: Dict[type, "Singleton"],
    ):
        Singleton.set_state(singleton_state)
        configure_log(self.config.hydra.job_logging, self.config.hydra.verbose)
        setup_globals()
        sweep_config = self.config_loader.load_sweep_config(
            self.config, sweep_overrides
        )
        with open_dict(sweep_config.hydra.job) as job:
            # Populate new job variables
            if "SLURM_JOB_ID" in os.environ:
                job.id = os.environ["SLURM_JOB_ID"]
            else:
                job.id = "unknown"
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
        queue_parameters = self.queue_parameters.copy()
        OmegaConf.set_struct(queue_parameters, True)
        if self.queue == "auto":
            max_num_timeout = self.queue_parameters.auto.max_num_timeout
            with open_dict(queue_parameters):
                del queue_parameters.auto["max_num_timeout"]
            executor = submitit.AutoExecutor(
                folder=self.folder, max_num_timeout=max_num_timeout
            )
        elif self.queue == "slurm":
            max_num_timeout = self.queue_parameters.slurm.max_num_timeout
            with open_dict(queue_parameters):
                del queue_parameters.slurm["max_num_timeout"]
            executor = submitit.SlurmExecutor(
                folder=self.folder, max_num_timeout=max_num_timeout
            )
        elif self.queue == "local":
            executor = submitit.LocalExecutor(folder=self.folder)
        else:
            raise RuntimeError("Unsupported queue type {}".format(self.queue))

        executor.update_parameters(**queue_parameters[self.queue])

        log.info("Sweep output dir : {}".format(self.config.hydra.sweep.dir))
        path_str = str(self.config.hydra.sweep.dir)
        os.makedirs(path_str, exist_ok=True)
        if "mode" in self.config.hydra.sweep:
            mode = int(str(self.config.hydra.sweep.mode), 8)
            os.chmod(path_str, mode=mode)

        params = []
        for job_num in range(num_jobs):
            sweep_override = list(job_overrides[job_num])
            log.info(
                "\t#{} : {}".format(
                    job_num, " ".join(filter_overrides(sweep_override)),
                )
            )
            params.append(
                (sweep_override, "hydra.sweep.dir", job_num, Singleton.get_state(),)
            )
        jobs = executor.map_array(self, *zip(*params))
        return [j.results()[0] for j in jobs]
