# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Sequence

import cloudpickle  # type: ignore
import pickle5 as pickle  # type: ignore
from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, configure_log, filter_overrides, setup_globals
from omegaconf import OmegaConf, open_dict, read_write

from hydra_plugins.hydra_ray_launcher._launcher_util import (  # type: ignore
    JOB_RETURN_PICKLE,
    JOB_SPEC_PICKLE,
    ray_down,
    ray_exec,
    ray_rsync_down,
    ray_rsync_up,
    ray_tmp_dir,
    ray_up,
    rsync,
)
from hydra_plugins.hydra_ray_launcher.ray_aws_launcher import (  # type: ignore
    RayAWSLauncher,
)

log = logging.getLogger(__name__)


def _get_abs_code_dir(code_dir: str) -> str:
    if code_dir:
        if os.path.isabs(code_dir):
            return code_dir
        else:
            return os.path.join(os.getcwd(), code_dir)
    else:
        return ""


def _pickle_jobs(tmp_dir: str, **jobspec: Dict[Any, Any]) -> None:
    path = os.path.join(tmp_dir, JOB_SPEC_PICKLE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        cloudpickle.dump(jobspec, f)
    log.info(f"Pickle for jobs: {f.name}")


def launch(
    launcher: RayAWSLauncher,
    job_overrides: Sequence[Sequence[str]],
    initial_job_idx: int,
) -> Sequence[JobReturn]:
    setup_globals()
    assert launcher.config is not None
    assert launcher.config_loader is not None
    assert launcher.task_function is not None

    setup_commands = launcher.mandatory_install.install_commands
    setup_commands.extend(launcher.ray_cluster_cfg.setup_commands)

    with read_write(launcher.ray_cluster_cfg):
        launcher.ray_cluster_cfg.setup_commands = setup_commands

    configure_log(launcher.config.hydra.hydra_logging, launcher.config.hydra.verbose)

    log.info(f"Ray Launcher is launching {len(job_overrides)} jobs, ")

    with tempfile.TemporaryDirectory() as local_tmp_dir:
        sweep_configs = []
        for idx, overrides in enumerate(job_overrides):
            idx = initial_job_idx + idx
            ostr = " ".join(filter_overrides(overrides))
            log.info(f"\t#{idx} : {ostr}")
            sweep_config = launcher.config_loader.load_sweep_config(
                launcher.config, list(overrides)
            )
            with open_dict(sweep_config):
                # job.id will be set on the EC2 instance before running the job.
                sweep_config.hydra.job.num = idx

            sweep_configs.append(sweep_config)

        _pickle_jobs(
            tmp_dir=local_tmp_dir,
            sweep_configs=sweep_configs,  # type: ignore
            task_function=launcher.task_function,
            singleton_state=Singleton.get_state(),
        )

        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            with open(f.name, "w") as file:
                OmegaConf.save(
                    config=launcher.ray_cluster_cfg, f=file.name, resolve=True
                )
            launcher.ray_yaml_path = f.name
            log.info(
                f"Saving RayClusterConf in a temp yaml file: {launcher.ray_yaml_path}."
            )

            return launch_jobs(
                launcher, local_tmp_dir, Path(HydraConfig.get().sweep.dir)
            )


def launch_jobs(
    launcher: RayAWSLauncher, local_tmp_dir: str, sweep_dir: Path
) -> Sequence[JobReturn]:
    ray_up(launcher.ray_yaml_path)
    with tempfile.TemporaryDirectory() as local_tmp_download_dir:

        with ray_tmp_dir(
            launcher.ray_yaml_path, launcher.docker_enabled
        ) as remote_tmp_dir:

            ray_rsync_up(
                launcher.ray_yaml_path, os.path.join(local_tmp_dir, ""), remote_tmp_dir
            )

            script_path = os.path.join(os.path.dirname(__file__), "_remote_invoke.py")
            ray_rsync_up(launcher.ray_yaml_path, script_path, remote_tmp_dir)

            if launcher.sync_up.source_dir:
                source_dir = _get_abs_code_dir(launcher.sync_up.source_dir)
                target_dir = (
                    launcher.sync_up.target_dir
                    if launcher.sync_up.target_dir
                    else remote_tmp_dir
                )
                rsync(
                    launcher.ray_yaml_path,
                    launcher.sync_up.include,
                    launcher.sync_up.exclude,
                    os.path.join(source_dir, ""),
                    target_dir,
                )

            ray_exec(
                launcher.ray_yaml_path,
                launcher.docker_enabled,
                os.path.join(remote_tmp_dir, "_remote_invoke.py"),
                remote_tmp_dir,
            )

            ray_rsync_down(
                launcher.ray_yaml_path,
                os.path.join(remote_tmp_dir, JOB_RETURN_PICKLE),
                local_tmp_download_dir,
            )

            sync_down_cfg = launcher.sync_down

            if (
                sync_down_cfg.target_dir
                or sync_down_cfg.source_dir
                or sync_down_cfg.include
                or sync_down_cfg.exclude
            ):
                source_dir = (
                    sync_down_cfg.source_dir if sync_down_cfg.source_dir else sweep_dir
                )
                target_dir = (
                    sync_down_cfg.source_dir if sync_down_cfg.source_dir else sweep_dir
                )
                target_dir = Path(_get_abs_code_dir(target_dir))
                target_dir.mkdir(parents=True, exist_ok=True)

                rsync(
                    launcher.ray_yaml_path,
                    launcher.sync_down.include,
                    launcher.sync_down.exclude,
                    os.path.join(source_dir),
                    str(target_dir),
                    up=False,
                )
                log.info(
                    f"Syncing outputs from remote dir: {source_dir} to local dir: {target_dir.absolute()} "
                )

        if launcher.stop_cluster:
            log.info("Stopping cluster now. (stop_cluster=true)")
            if launcher.ray_cluster_cfg.provider.cache_stopped_nodes:
                log.info("NOT deleting the cluster (provider.cache_stopped_nodes=true)")
            else:
                log.info("Deleted the cluster (provider.cache_stopped_nodes=false)")
            ray_down(launcher.ray_yaml_path)
        else:
            log.warning(
                "NOT stopping cluster, this may incur extra cost for you. (stop_cluster=false)"
            )

        with open(os.path.join(local_tmp_download_dir, JOB_RETURN_PICKLE), "rb") as f:
            job_returns = pickle.load(f)  # nosec
            assert isinstance(job_returns, List)
            for run in job_returns:
                assert isinstance(run, JobReturn)
            return job_returns
