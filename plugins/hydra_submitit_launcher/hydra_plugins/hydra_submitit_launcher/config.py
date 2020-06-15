# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from hydra.core.config_store import ConfigStore
from hydra.types import ObjectConf


class ExecutorName(Enum):
    local = "local"
    slurm = "slurm"


@dataclass
class BaseSubmititConf:
    """Configuration shared by all executors
    """

    # maximum time for the job in minutes
    timeout_min: Optional[int] = None
    # number of cpus to use for each task
    cpus_per_task: Optional[int] = None
    # number of gpus to use on each node
    gpus_per_node: Optional[int] = None
    # number of tasks to spawn on each node
    tasks_per_node: Optional[int] = None
    # memory to reserve for the job on each node (in GB)
    mem_gb: Optional[int] = None
    # number of nodes to use for the job
    nodes: Optional[int] = None
    # name of the job
    name: Optional[str] = None


@dataclass
class SubmititSlurmConf(BaseSubmititConf):
    """Slurm configuration overrides and specific parameters
    """

    # Params are used to configure sbatch, for more info check:
    # https://github.com/facebookincubator/submitit/blob/master/submitit/slurm/slurm.py

    # Following parameters are slurm specific
    # More information: https://slurm.schedmd.com/sbatch.html
    #
    # slurm partition to use on the cluster
    partition: Optional[str] = None
    comment: Optional[str] = None
    constraint: Optional[str] = None
    exclude: Optional[str] = None

    # Following parameters are submitit specifics
    #
    # USR1 signal delay before timeout
    signal_delay_s: int = 120
    # Maximum number of retries on job timeout.
    # Change this only after you confirmed your code can handle re-submission
    # by properly resuming from the latest stored checkpoint.
    # check the following for more info on slurm_max_num_timeout
    # https://github.com/facebookincubator/submitit/blob/master/docs/checkpointing.md
    max_num_timeout: int = 0


@dataclass
class SubmititConf(BaseSubmititConf):
    folder: str = "${hydra.sweep.dir}/.${hydra.launcher.params.queue}"

    # executor to use (currently either "slurm" or "local" are supported,
    # None defaults to an available cluster)
    executor: ExecutorName = ExecutorName.slurm

    # maximum time for the job in minutes
    timeout_min: int = 60
    # number of cpus to use for each task
    cpus_per_task: int = 1
    # number of gpus to use on each node
    gpus_per_node: int = 0
    # number of tasks to spawn on each node
    tasks_per_node: int = 1
    # memory to reserve for the job on each node (in GB)
    mem_gb: int = 4
    # number of nodes to use for the job
    nodes: int = 1
    # name of the job
    name: str = "${hydra.job.name}"

    # additional specific parameters and overrides are
    # provided here
    local_executor: BaseSubmititConf = BaseSubmititConf()
    slurm_executor: SubmititSlurmConf = SubmititSlurmConf()


@dataclass
class SubmititLauncherConf(ObjectConf):
    cls: str = "hydra_plugins.hydra_submitit_launcher.submitit_launcher.SubmititLauncher"
    params: SubmititConf = SubmititConf()


ConfigStore.instance().store(
    group="hydra/launcher",
    name="submitit",
    node=SubmititLauncherConf,
    provider="submitit_launcher",
)
