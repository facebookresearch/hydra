# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from hydra.core.config_store import ConfigStore
from hydra.types import ObjectConf


class QueueType(Enum):
    auto = "auto"
    local = "local"
    slurm = "slurm"


@dataclass
class SlurmQueueConf:
    # Params are used to configure sbatch, for more info check:
    # https://github.com/facebookincubator/submitit/blob/master/submitit/slurm/slurm.py

    # maximum time for the job in minutes
    time: int = 60
    # number of cpus to use for each task
    cpus_per_task: int = 10
    # number of gpus to use on each node
    gpus_per_node: int = 1
    # number of tasks to spawn on each node
    ntasks_per_node: int = 1
    # number of nodes to use for the job
    nodes: int = 1
    # memory to reserve for the job on each node, in GB
    mem: str = "${hydra.launcher.mem_limit}GB"
    # slurm partition to use on the cluster
    partition: Optional[str] = None
    # USR1 signal delay before timeout
    signal_delay_s: int = 120
    # name of the job
    job_name: str = "${hydra.job.name}"
    # Maximum number of retries on job timeout.
    # Change this only after you confirmed your code can handle re-submission
    # by properly resuming from the latest stored checkpoint.
    # check the following for more info on slurm_max_num_timeout
    # https://github.com/facebookincubator/submitit/blob/master/docs/checkpointing.md
    max_num_timeout: int = 0


@dataclass
class LocalQueueConf:
    # local executor mocks the behavior of slurm locally

    # maximum time for the job in minutes
    timeout_min: int = 60
    # number of gpus to use on each node
    gpus_per_node: int = 1
    # number of tasks to spawn on each node (only one node available in local executor)
    tasks_per_node: int = 1


@dataclass
class AutoQueueConf:
    # auto executor automatically identifies and uses available cluster
    # Currently this is only slurm, but local executor can be manually forced
    # instead.
    # Most parameters are shared between clusters, some can be cluster specific

    # cluster to use (currently either "slurm" or "local" are supported,
    # None defaults to an available cluster)
    cluster: Optional[str] = None

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

    # following parameters are SLURM specific

    # Maximum number of retries on job timeout.
    # Change this only after you confirmed your code can handle re-submission
    # by properly resuming from the latest stored checkpoint.
    # check the following for more info on slurm_max_num_timeout
    # https://github.com/facebookincubator/submitit/blob/master/docs/checkpointing.md
    slurm_max_num_timeout: int = 0
    # USR1 signal delay before timeout for the slurm queue
    slurm_signal_delay_s: int = 30
    # slurm partition to use on the cluster
    slurm_partition: Optional[str] = None


@dataclass
class QueueParams:
    slurm: SlurmQueueConf = SlurmQueueConf()
    local: LocalQueueConf = LocalQueueConf()
    auto: AutoQueueConf = AutoQueueConf()


@dataclass
class SubmititConf:
    queue: QueueType = QueueType.local

    folder: str = "${hydra.sweep.dir}/.${hydra.launcher.params.queue}"

    queue_parameters: QueueParams = QueueParams()


@dataclass
class SubmititLauncherConf(ObjectConf):
    cls: str = "hydra_plugins.hydra_submitit_launcher.submitit_launcher.SubmititLauncher"
    params: SubmititConf = SubmititConf()
    mem_limit: int = 2


ConfigStore.instance().store(
    group="hydra/launcher",
    name="submitit",
    node=SubmititLauncherConf,
    provider="submitit_launcher",
)
