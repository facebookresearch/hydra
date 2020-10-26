# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
from contextlib import contextmanager
from subprocess import PIPE, Popen
from typing import Any, Dict, Generator, List, Tuple

import ray
from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, run_job, setup_globals
from hydra.types import TaskFunction
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)

JOB_SPEC_PICKLE = "job_spec.pkl"
JOB_RETURN_PICKLE = "returns.pkl"


def start_ray(ray_init_cfg: DictConfig) -> None:
    if not ray.is_initialized():
        log.info(f"Initializing ray with config: {ray_init_cfg}")
        if ray_init_cfg:
            ray.init(**ray_init_cfg)
        else:
            ray.init()
    else:
        log.info("Ray is already running.")


def _run_job(
    sweep_config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Dict[Any, Any],
) -> JobReturn:
    setup_globals()
    Singleton.set_state(singleton_state)
    HydraConfig.instance().set_config(sweep_config)
    return run_job(
        config=sweep_config,
        task_function=task_function,
        job_dir_key="hydra.sweep.dir",
        job_subdir_key="hydra.sweep.subdir",
    )


def launch_job_on_ray(
    ray_remote_cfg: DictConfig,
    sweep_config: DictConfig,
    task_function: TaskFunction,
    singleton_state: Any,
) -> Any:
    if ray_remote_cfg:
        run_job_ray = ray.remote(**ray_remote_cfg)(_run_job)
    else:
        run_job_ray = ray.remote(_run_job)

    ret = run_job_ray.remote(
        sweep_config=sweep_config,
        task_function=task_function,
        singleton_state=singleton_state,
    )
    return ret


def _run_command(args: Any) -> Tuple[str, str]:
    with Popen(args=args, stdout=PIPE, stderr=PIPE) as proc:
        log.info(f"Running command: {args}")
        out, err = proc.communicate()
        out_str = out.decode().strip() if out is not None else ""
        err_str = err.decode().strip() if err is not None else ""
        log.info(f"Output: {out_str} \n Error: {err_str}")
        return out_str, err_str


def ray_rsync_down(yaml_path: str, remote_dir: str, local_dir: str) -> None:
    args = ["ray", "rsync-down"]
    args += [yaml_path, remote_dir, local_dir]
    _run_command(args)


@contextmanager
def ray_tmp_dir(yaml_path: str, docker: bool) -> Generator[Any, None, None]:
    args = ["ray", "exec"]
    if docker:
        args.append("--docker")

    mktemp_args = args + [yaml_path, "echo $(mktemp -d)"]
    out, _ = _run_command(mktemp_args)
    tmppath = [
        x
        for x in out.strip().split()
        if x.startswith("/tmp/") and "ray-config" not in x  # nosec
    ]
    assert len(tmppath) == 1, f"tmppath is : {tmppath}"
    tmp_path = tmppath[0]
    log.info(f"Created temp path on remote server {tmp_path}")
    yield tmp_path
    rmtemp_args = args + [yaml_path, f"rm -rf {tmp_path}"]
    _run_command(rmtemp_args)


def ray_new_dir(yaml_path: str, new_dir: str, docker: bool) -> None:
    """
    The output of exec os.getcwd() via ray on remote cluster.
    """
    args = ["ray", "exec"]
    if docker:
        args += "--docker"

    mktemp_args = args + [yaml_path, f"mkdir -p {new_dir}"]
    _run_command(mktemp_args)


def ray_rsync_up(yaml_path: str, local_dir: str, remote_dir: str) -> None:
    _run_command(["ray", "rsync-up", yaml_path, local_dir, remote_dir])


def ray_down(yaml_path: str) -> None:
    _run_command(["ray", "down", "-y", yaml_path])


def ray_up(yaml_path: str) -> None:
    _run_command(["ray", "up", "-y", yaml_path])


def ray_exec(yaml_path: str, docker: bool, file_path: str, pickle_path: str) -> None:
    command = f"python {file_path} {pickle_path}"
    args = ["ray", "exec"]
    if docker:
        args.append("--docker")
    args += [yaml_path, command]
    _run_command(args)


def _ray_get_head_ip(yaml_path: str) -> str:
    out, _ = _run_command(["ray", "get-head-ip", yaml_path])
    return out.strip()


def _get_pem(ray_cluster_cfg: Any) -> Any:
    key_name = ray_cluster_cfg.auth.get("ssh_private_key")
    if key_name is not None:
        return key_name
    key_name = ray_cluster_cfg.provider.get("key_pair", {}).get("key_name")
    if key_name:
        return os.path.expanduser(os.path.expanduser(f"~/.ssh/{key_name}.pem"))
    region = ray_cluster_cfg.provider.region
    key_pair_name = f"ray-autoscaler_{region}"
    return os.path.expanduser(f"~/.ssh/{key_pair_name}.pem")


def rsync(
    yaml_path: str,
    include: List[str],
    exclude: List[str],
    source: str,
    target: str,
    up: bool = True,
) -> None:
    ray_cluster_cfg = OmegaConf.load(yaml_path)
    keypair = _get_pem(ray_cluster_cfg)
    remote_ip = _ray_get_head_ip(yaml_path)
    user = ray_cluster_cfg.auth.ssh_user
    args = ["rsync", "--rsh", f"ssh -i {keypair}  -o StrictHostKeyChecking=no", "-avz"]

    for i in include:
        args += [f"--include={i}"]
    for e in exclude:
        args += [f"--exclude={e}"]

    args += ["--prune-empty-dirs"]

    if up:
        target = f"{user}@{remote_ip}:{target}"
    else:
        source = f"{user}@{remote_ip}:{source}"
    args += [source, target]
    _run_command(args)
