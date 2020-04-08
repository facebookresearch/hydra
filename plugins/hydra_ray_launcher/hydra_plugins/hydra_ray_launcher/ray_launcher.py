# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import tempfile
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Any, Dict, Sequence

import cloudpickle
from omegaconf import DictConfig, OmegaConf, open_dict

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, configure_log, filter_overrides, setup_globals
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.types import TaskFunction


log = logging.getLogger(__name__)


class RayLauncherSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "hydra-ray-launcher", "pkg://hydra_plugins.hydra_ray_launcher.conf"
        )


class RayLauncher(Launcher):
    def __init__(self,
                 mode: str,
                 modes: DictConfig) -> None:
        self.config = None
        self.task_function = None
        self.config_loader = None
        self.mode = mode
        cluster_config = modes.get(mode)
        # TODO make it support local
        if mode == "aws":
            self.ray_cluster_config = cluster_config.get("ray_cluster_config")
            self.ray_init_config = cluster_config.get("ray_init_config")
            self.ray_remote_config = cluster_config.get("ray_remote_config")

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        setup_globals()
        assert self.config is not None
        assert self.config_loader is not None
        assert self.task_function is not None

        # based on mode, populate self.ray_yaml_path
        ray_yaml_path = self._save_ray_config()

        # Add remote dir to the search path. TODO see if there's a better way to do this
        remote_script_dir = self._get_remote_dir(ray_yaml_path)

        configure_log(self.config.hydra.hydra_logging, self.config.hydra.verbose)
        sweep_dir = Path(str(self.config.hydra.sweep.dir))
        sweep_dir.mkdir(parents=True, exist_ok=True)
        log.info("Ray Launcher is launching {} jobs".format(len(job_overrides)))
        log.info("Sweep output dir : {}".format(sweep_dir))

        temp_dir_job_dump = tempfile.mkdtemp()

        for idx, overrides in enumerate(job_overrides):
            idx = initial_job_idx + idx
            log.info("\t#{} : {}".format(idx, " ".join(filter_overrides(overrides))))
            sweep_config = self.config_loader.load_sweep_config(
                self.config, list(overrides)
            )
            with open_dict(sweep_config):
                # This typically coming from the underlying scheduler (SLURM_JOB_ID for instance)
                # In that case, it will not be available here because we are still in the main process.
                # but instead should be populated remotely before calling the task_function.
                sweep_config.hydra.job.id = "job_id_for_{}".format(idx)
                sweep_config.hydra.job.num = idx
            HydraConfig.instance().set_config(sweep_config)
            singleton_state = Singleton.get_state()
            self._dump_func_params(
                idx,
                sweep_config,
                self.config,
                self.task_function,
                singleton_state,
                temp_dir_job_dump,
            )

        remote_pickle_dir = self._get_remote_dir(ray_yaml_path)
        self._rsync_to_ray_cluster(
            os.path.join(temp_dir_job_dump, ""), remote_pickle_dir, ray_yaml_path
        )

        self._rsync_to_ray_cluster(
            os.path.join(os.path.dirname(__file__), "ray_remote_invoke.py"),
            remote_script_dir,
            ray_yaml_path,
        )

        self._invoke_functions_on_ray(
            ray_yaml_path,
            os.path.join(remote_script_dir, "ray_remote_invoke.py"),
            remote_pickle_dir,
        )
        # the script running on Ray cluster cannot pass result back to our local machine.
        return []

    def _invoke_functions_on_ray(
        self, yaml_file_path: str, file_path: str, pickle_path: str
    ):
        command = "python {} {}".format(file_path, pickle_path)
        log.info("Issuing command on remote server: {}".format(command))
        ray_proc = Popen(
            [
                "ray",
                "exec",
                yaml_file_path,
                "python {} {}".format(file_path, pickle_path),
            ],
            stdin=PIPE,
            stdout=PIPE,
        )
        out, err = ray_proc.communicate()
        log.info("invoking script on ray cluster out: {}, err: {}".format(out, err))

    def _get_remote_dir(self, yaml_file_path: str) -> str:
        ray_proc = Popen(
            ["ray", "exec", yaml_file_path, "echo $(mktemp -d)"],
            stdin=PIPE,
            stdout=PIPE,
        )
        out, err = ray_proc.communicate()
        return out.decode().strip()

    def _rsync_to_ray_cluster(
        self, local_dir: str, remote_dir: str, yaml_file_path: str
    ) -> None:
        ray_proc = Popen(
            ["ray", "rsync-up", yaml_file_path, local_dir, remote_dir],
            stdin=PIPE,
            stdout=PIPE,
        )
        out, err = ray_proc.communicate()
        log.info(
            "rsync dir to ray cluster. source : {}, target: {}, ray config yaml: {}. out: {}, err: {}".format(
                local_dir, remote_dir, yaml_file_path, out, err
            )
        )

    def _dump_func_params(
        self,
        idx: int,
        sweep_config: DictConfig,
        config: DictConfig,
        task_function: TaskFunction,
        singleton_state: Dict[Any, Any],
        temp_dir: str,
    ) -> str:
        path = os.path.join(temp_dir, str(idx), "params.pkl")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            params_dict = {
                "idx": idx,
                "sweep_config": sweep_config,
                "config": config,
                "task_function": task_function,
                "singleton_state": singleton_state,
            }
            cloudpickle.dump(params_dict, f)
        log.info("Pickle for job {}: {}".format(idx, f.name))

    def _save_ray_config(self) -> str:
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            with open(f.name, "w") as file:
                print(OmegaConf.create(self.ray_cluster_config).pretty(), file=file)

            log.info("Ray cluster yaml : {}".format(f.name))
            # call 'ray up cluster.yaml' to update the cluster
            ray_up_proc = Popen(["ray", "up", f.name], stdin=PIPE, stdout=PIPE)
            # y to the prompt asking if we want to restart ray server
            ray_up_proc.communicate(input=b"y")
            return f.name

