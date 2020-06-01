# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from enum import Enum

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
    nodes: int = 1
    gpus_per_node: int = 1
    ntasks_per_node: int = 1
    mem: str = "${hydra.launcher.mem_limit}GB"
    cpus_per_task: int = 10
    time: int = 60
    partition: str = "dev"
    signal_delay_s: int = 120
    job_name: str = "${hydra.job.name}"
    # Maximum number of retries on job timeout.
    # Change this only after you confirmed your code can handle re-submission
    # by properly resuming from the latest stored checkpoint.
    max_num_timeout: int = 0


@dataclass
class LocalQueueConf:
    gpus_per_node: int = 1
    tasks_per_node: int = 1
    timeout_min: int = 60


@dataclass
class AutoQueueConf:
    # check the following for more info on slurm_max_num_timeout
    # https://github.com/facebookincubator/submitit/blob/master/docs/checkpointing.md
    slurm_max_num_timeout: int = 0
    gpus_per_node: int = 1
    timeout_min: int = 60


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
