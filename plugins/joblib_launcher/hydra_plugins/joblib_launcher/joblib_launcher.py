# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from joblib import Parallel, delayed  # type: ignore
from omegaconf import DictConfig, open_dict

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.hydra_config import HydraConfig
from hydra.core.utils import (
    JobReturn,
    JobRuntime,
    configure_log,
    filter_overrides,
    run_job,
    setup_globals,
)
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.types import TaskFunction

log = logging.getLogger(__name__)


class JoblibLauncherSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the JoblibLauncher plugin to be discovered
    and used once the JoblibLauncher plugin is installed
    """

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-joblib-launcher", "pkg://hydra_plugins.joblib_launcher_plugin.conf",
        )


class JoblibLauncher(Launcher):
    def __init__(self, **kwargs_joblib_parallel: Any) -> None:
        """Parallel Launcher

        Keyword arguments that are not None are passed to joblib.Parallel

        For details, refer to to the Parallel documentation:
        https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html
        """
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None

        self.kwargs_joblib_parallel = {}
        for keyword, value in kwargs_joblib_parallel.items():
            if value is not None:
                self.kwargs_joblib_parallel[keyword] = value

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function

    def launch(self, job_overrides: Sequence[Sequence[str]]) -> Sequence[JobReturn]:
        """
        :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
        :return: an array of return values from run_job with indexes corresponding to the input list indexes.
        """
        setup_globals()
        assert self.config is not None
        assert self.config_loader is not None
        assert self.task_function is not None

        configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        sweep_dir = Path(str(self.config.hydra.sweep.dir))
        sweep_dir.mkdir(parents=True, exist_ok=True)
        log.info(
            "JoblibLauncher({}) is launching {} jobs".format(
                ",".join([f"{k}={v}" for k, v in self.kwargs_joblib_parallel.items()]),
                len(job_overrides),
            )
        )
        log.info("Sweep output dir : {}".format(sweep_dir))

        job_runtime = {"name": JobRuntime.instance().get("name")}

        runs = Parallel(**self.kwargs_joblib_parallel)(
            delayed(dispatch_job)(
                idx,
                overrides,
                self.config_loader,
                self.config,
                self.task_function,
                job_runtime,
            )
            for idx, overrides in enumerate(job_overrides)
        )

        return runs  # type: ignore


def dispatch_job(
    idx: int,
    overrides: Sequence[str],
    config_loader: ConfigLoader,
    config: DictConfig,
    task_function: TaskFunction,
    job_runtime: Dict[str, Any],
) -> JobReturn:
    """Calls `run_job` through Joblib Parallel backend

    Note that Joblib's default backend runs isolated Python processes, see
    https://joblib.readthedocs.io/en/latest/parallel.html#shared-memory-semantics
    """
    # JobRuntime uses a singleton pattern and thus needs to be re-created
    JobRuntime.instance().set("name", job_runtime["name"])

    # Similarly, setup_globals() registering OmegaConf resolvers is called again
    setup_globals()

    log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(overrides))))
    sweep_config = config_loader.load_sweep_config(config, list(overrides))
    with open_dict(sweep_config):
        sweep_config.hydra.job.id = "job_id_for_{}".format(idx)
        sweep_config.hydra.job.num = idx
    HydraConfig.instance().set_config(sweep_config)

    ret = run_job(
        config=sweep_config,
        task_function=task_function,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )

    configure_log(config.hydra.hydra_logging, config.hydra.verbose)

    return ret
