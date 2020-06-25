# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from pathlib import Path
from typing import Optional, Sequence, Any, Dict, List

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.hydra_config import HydraConfig
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
from hydra.types import TaskFunction
from omegaconf import DictConfig, open_dict
import subprocess
import os
import sys
import hydra
import time

from joblib import Parallel, delayed

# IMPORTANT:
# If your plugin imports any module that takes more than a fraction of a second to import,
# Import the module lazily (typically inside launch()).
# Installed plugins are imported during Hydra initialization and plugins that are slow to import plugins will slow
# the startup of ALL hydra applications.
# Another approach is to place heavy includes in a file prefixed by _, such as _core.py:
# Hydra will not look for plugin in such files and will not import them during plugin discovery.


log = logging.getLogger(__name__)

def look_for_task_spooler():
    """
    Task spooler is known as `tsp` on Ubuntu and `ts` on MacOS. 
    This function checks for which one exists and returns the
    valid command, or throws an error if neither is found.

    Returns:
        str: Either `ts` or `tsp` depending on which is valid.

    Raises:
        RuntimeError when TaskSpooler isn't found on the system.
    """
    commands = {'ts': False, 'tsp': False}

    for c in commands:
        try:
            cmd_output = str(subprocess.check_output([c, '-h']))
            if 'usage' in cmd_output:
                commands[c] = True
        except:
            commands[c] = False
    
    if not any(commands.values()):
        raise RuntimeError("Task spooler not found! Install it to use this launcher.")
    
    for c in commands:
        if commands[c]:
            return c

def _get_job_status(tsp_prefix, job_id):
    job_status = subprocess.check_output(
        f"{tsp_prefix} -s {job_id}", shell=True)
    return job_status.rstrip().decode('utf-8')

def execute_job(
    idx: int,
    overrides: Sequence[str],
    config_loader: ConfigLoader,
    config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
    cmd_prefix: str,
    tsp_prefix: str,
) -> JobReturn:
    """Calls `run_job` in parallel
    """
    setup_globals()
    Singleton.set_state(singleton_state)

    lst = " ".join(filter_overrides(overrides))

    sweep_config = config_loader.load_sweep_config(config, list(overrides))
    with open_dict(sweep_config):
        sweep_config.hydra.job.id = "{}_{}".format(sweep_config.hydra.job.name, idx)
        sweep_config.hydra.job.num = idx
    HydraConfig.instance().set_config(sweep_config)

    def tsp_task_function(task_cfg):
        working_dir = os.getcwd()
        lst = " ".join([f'{k}={v}' for k, v in task_cfg.items()])
        cmd = f"{cmd_prefix} {lst}"
        log.info(f"\t#{idx} : {lst}")
        cmd = f"cd {hydra.utils.get_original_cwd()} && {cmd} hydra.run.dir={working_dir}"
        job_id = int(subprocess.check_output(cmd, shell=True).rstrip())
        log.info(f"Submitted {idx} to TaskSpooler with task ID {job_id} -> {cmd}")
        return job_id

    ret = run_job(
        config=sweep_config,
        task_function=tsp_task_function,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )

    return ret

class TaskSpoolerLauncherSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleLauncher plugin to be discovered
    and used once the ExampleLauncher plugin is installed
    """

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-tsp-launcher",
            "pkg://hydra_plugins.hydra_tsp_launcher.conf",
        )

class TaskSpoolerLauncher(Launcher):
    def __init__(self, max_workers : int = None, time_between_submit : int = 0) -> None:
        self.config: Optional[DictConfig] = None
        self.config_loader: Optional[ConfigLoader] = None
        self.task_function: Optional[TaskFunction] = None
        self.max_workers = max_workers
        self.time_between_submit = time_between_submit

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function

        self.cmd_prefix = f"{sys.executable} {sys.argv[0]}"
        self.tsp_prefix = look_for_task_spooler()
        self.cmd_prefix = f"{self.tsp_prefix} {self.cmd_prefix}"

    def tail_job(self, job_id):
        job_status = _get_job_status(self.tsp_prefix, job_id)
        while job_status == 'queued':
            time.sleep(1)
            job_status = _get_job_status(self.tsp_prefix, job_id)
        
        log.info(f"{job_id} has status {job_status}")
        subprocess.call(
            f"{self.tsp_prefix} -t {job_id}", shell=True
        )

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        """
        :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
        :param initial_job_idx: Initial job idx in batch.
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
            f"TaskSpooler Launcher is launching {len(job_overrides)} jobs locally"
        )
        log.info(f"Sweep output dir : {sweep_dir}")
        runs = []
        singleton_state = Singleton.get_state()        

        for idx, overrides in enumerate(job_overrides):
            ret = execute_job(
                initial_job_idx + idx,
                overrides,
                self.config_loader,
                self.config,
                self.task_function,
                singleton_state,
                self.cmd_prefix,
                self.tsp_prefix,
            )
            runs.append(ret)
        
        assert isinstance(runs, List)
        for run in runs:
            assert isinstance(run, JobReturn)

        runs = Parallel(n_jobs=len(job_overrides), backend='threading')(
            delayed(self.tail_job)(
                run.return_value
            )
            for run in runs
        )
        
        return runs
