# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Sequence

import cloudpickle  # type: ignore
import pickle5 as pickle  # type: ignore
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, configure_log, filter_overrides, setup_globals
from omegaconf import OmegaConf, open_dict, read_write
from ray.autoscaler import sdk

from hydra_plugins.hydra_ray_launcher._launcher_util import (  # type: ignore
    JOB_RETURN_PICKLE,
    JOB_SPEC_PICKLE,
    ray_tmp_dir,
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

    setup_commands = launcher.env_setup.commands
    packages = filter(
        lambda x: x[1] is not None, launcher.env_setup.pip_packages.items()
    )
    with read_write(setup_commands):
        setup_commands.extend(
            [f"pip install {package}=={version}" for package, version in packages]
        )
        setup_commands.extend(launcher.ray_cfg.cluster.setup_commands)

    with read_write(launcher.ray_cfg.cluster):
        launcher.ray_cfg.cluster.setup_commands = setup_commands

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
                    config=launcher.ray_cfg.cluster, f=file.name, resolve=True
                )
            launcher.ray_yaml_path = f.name
            log.info(
                f"Saving RayClusterConf in a temp yaml file: {launcher.ray_yaml_path}."
            )

            return launch_jobs(
                launcher, local_tmp_dir, Path(launcher.config.hydra.sweep.dir)
            )


def launch_jobs(
    launcher: RayAWSLauncher, local_tmp_dir: str, sweep_dir: Path
) -> Sequence[JobReturn]:
    config = OmegaConf.to_container(
        launcher.ray_cfg.cluster, resolve=True, enum_to_str=True
    )
    sdk.create_or_update_cluster(
        config,
        no_restart=launcher.no_restart,
        restart_only=launcher.restart_only,
        no_config_cache=True,
    )
    with tempfile.TemporaryDirectory() as local_tmp_download_dir:

        with ray_tmp_dir(config) as remote_tmp_dir:
            sdk.rsync(
                config,
                source=os.path.join(local_tmp_dir, ""),
                target=remote_tmp_dir,
                down=False,
            )

            script_path = os.path.join(os.path.dirname(__file__), "_remote_invoke.py")
            remote_script_path = os.path.join(remote_tmp_dir, "_remote_invoke.py")
            sdk.rsync(config, source=script_path, target=remote_script_path, down=False)

            if launcher.sync_up.source_dir:
                source_dir = _get_abs_code_dir(launcher.sync_up.source_dir)
                target_dir = (
                    launcher.sync_up.target_dir
                    if launcher.sync_up.target_dir
                    else remote_tmp_dir
                )
                config["rsync_exclude"] = OmegaConf.to_container(
                    launcher.sync_up.exclude, resolve=True
                )
                sdk.rsync(
                    config,
                    source=os.path.join(source_dir, ""),
                    target=target_dir,
                    down=False,
                )
            sdk.run_on_cluster(
                config, cmd=f"python {remote_script_path} {remote_tmp_dir}"
            )

            sdk.rsync(
                config,
                source=os.path.join(remote_tmp_dir, JOB_RETURN_PICKLE),
                target=local_tmp_download_dir,
                down=True,
            )

            sync_down_cfg = launcher.sync_down

            if (
                sync_down_cfg.target_dir
                or sync_down_cfg.source_dir
                or sync_down_cfg.exclude
            ):
                source_dir = (
                    sync_down_cfg.source_dir if sync_down_cfg.source_dir else sweep_dir
                )
                target_dir = (
                    sync_down_cfg.target_dir if sync_down_cfg.target_dir else sweep_dir
                )
                target_dir = Path(_get_abs_code_dir(target_dir))
                target_dir.mkdir(parents=True, exist_ok=True)

                config["rsync_exclude"] = OmegaConf.to_container(
                    launcher.sync_down.exclude, resolve=True
                )
                sdk.rsync(
                    config,
                    source=os.path.join(source_dir, ""),
                    target=str(target_dir),
                    down=True,
                )

                log.info(
                    f"Syncing outputs from remote dir: {source_dir} to local dir: {target_dir.absolute()} "
                )

        if launcher.stop_cluster:
            log.info("Stopping cluster now. (stop_cluster=true)")
            if launcher.ray_cfg.cluster.provider.cache_stopped_nodes:
                log.info("NOT deleting the cluster (provider.cache_stopped_nodes=true)")
            else:
                log.info("Deleted the cluster (provider.cache_stopped_nodes=false)")
            sdk.teardown_cluster(config)
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
