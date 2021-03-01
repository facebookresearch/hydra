# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

import cloudpickle  # type: ignore
import hydra
import omegaconf
import pkg_resources
import ray
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING


@dataclass
class RayConf:
    init: Dict[str, Any] = field(default_factory=lambda: {"address": None})
    remote: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RayLauncherConf:
    _target_: str = "hydra_plugins.hydra_ray_launcher.ray_launcher.RayLauncher"
    ray: RayConf = RayConf()


# Ray AWS config, more info on ray's schema here:
# https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/ray-schema.json


class RayAutoScalingMode(Enum):
    default = "default"
    aggressive = "aggressive"


@dataclass
class RayDockerConf:
    """
    This executes all commands on all nodes in the docker container,
    and opens all the necessary ports to support the Ray cluster.
    Empty string means disabled.

    """

    # e.g., tensorflow/tensorflow:1.5.0-py3
    image: str = ""
    # e.g. ray_docker
    container_name: str = ""
    # If true, pulls latest version of image. Otherwise, `docker run` will only pull the image
    # if no cached version is present.
    pull_before_run: bool = True
    # Extra options to pass into "docker run"
    run_options: List[str] = field(default_factory=list)


@dataclass
class RayProviderConf:
    type: str = "aws"
    region: str = "us-west-2"
    availability_zone: str = "us-west-2a,us-west-2b"
    cache_stopped_nodes: bool = False
    key_pair: Dict[str, str] = field(
        default_factory=lambda: {"key_name": "hydra-${env:USER,user}"}
    )


@dataclass
class RsyncConf:
    """
    If your code contains more than one modules/files, you need to sync your code to the remote cluster.
    The code will be synced to a tmp dir on the cluster.
    code_dir could be a relative dir to where you run your app or a absolute dir.
    Leave this empty if you don't need to sync code.

    The conf is equivalent to run:
    rsync {source} {target} --include={include} --exclude={exclude}

    source/target will either be remote/local or local/remote depending on sync_up or sync down
    Read RayAWSConf for more details.
    """

    source_dir: Optional[str] = None
    target_dir: Optional[str] = None
    include: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)


@dataclass
class EnvSetupConf:
    pip_packages: Dict[str, str] = field(
        default_factory=lambda: {
            "omegaconf": omegaconf.__version__,
            "hydra_core": hydra.__version__,
            "ray": ray.__version__,
            "cloudpickle": cloudpickle.__version__,
            "pickle5": pkg_resources.get_distribution("pickle5").version,
            "hydra_ray_launcher": pkg_resources.get_distribution(
                "hydra_ray_launcher"
            ).version,
        }
    )

    commands: List[str] = field(
        default_factory=lambda: [
            "conda create -n hydra_${python_version:micro} python=${python_version:micro} -y",
            "echo 'export PATH=\"$HOME/anaconda3/envs/hydra_${python_version:micro}/bin:$PATH\"' >> ~/.bashrc",
        ]
    )


class RayRunEnv(Enum):
    """
    https://docs.ray.io/en/releases-1.1.0/package-ref.html?highlight=exec#ray-exec
    """

    auto = "auto"
    host = "host"
    docker = "docker"


@dataclass
class RayClusterConf:
    """
    This class maps to a Ray cluster config, e.g:
    https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/aws/example-full.yaml
    Schema: https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/ray-schema.json
    """

    # An unique identifier for the head node and workers of this cluster.
    cluster_name: str = "default"

    # The minimum number of workers nodes to launch in addition to the head
    # node. This number should be >= 0.
    min_workers: int = 0

    # The maximum number of workers nodes to launch in addition to the head
    # node. This takes precedence over min_workers.
    max_workers: int = 1

    # The initial number of worker nodes to launch in addition to the head
    # node. When the cluster is first brought up (or when it is refreshed with a
    # subsequent `ray up`) this number of nodes will be started.
    initial_workers: int = 0

    autoscaling_mode: RayAutoScalingMode = RayAutoScalingMode.default

    # The autoscaler will scale up the cluster to this target fraction of resource
    # usage. For example, if a cluster of 10 nodes is 100% busy and
    # target_utilization is 0.8, it would resize the cluster to 13. This fraction
    # can be decreased to increase the aggressiveness of upscaling.
    # This value must be less than 1.0 for scaling to happen.
    target_utilization_fraction: float = 0.8

    # If a node is idle for this many minutes, it will be removed.
    idle_timeout_minutes: int = 5

    docker: RayDockerConf = RayDockerConf()

    provider: RayProviderConf = RayProviderConf()

    # For additional options, check:
    # https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/aws/example-full.yaml
    auth: Dict[str, str] = field(default_factory=lambda: {"ssh_user": "ubuntu"})

    """
    Additional options in boto docs.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
    """
    head_node: Dict[str, Any] = field(
        default_factory=lambda: {
            "InstanceType": "m5.large",
            "ImageId": "ami-008d8ed4bd7dc2485",
        }
    )

    worker_nodes: Dict[str, Any] = field(
        default_factory=lambda: {
            "InstanceType": "m5.large",
            "ImageId": "ami-008d8ed4bd7dc2485",
        }
    )

    # Files or directories to copy to the head and worker nodes. The format is a
    # dictionary from REMOTE_PATH: LOCAL_PATH, e.g.
    file_mounts: Dict[str, str] = field(default_factory=dict)

    initialization_commands: List[str] = field(default_factory=list)

    setup_commands: List[str] = MISSING

    head_setup_commands: List[str] = field(default_factory=list)

    worker_setup_commands: List[str] = field(default_factory=list)

    head_start_ray_commands: List[str] = field(
        default_factory=lambda: [
            "ray stop",
            "ulimit -n 65536;ray start --head --port=6379 --object-manager-port=8076 \
            --autoscaling-config=~/ray_bootstrap_config.yaml",
        ]
    )

    # Custom commands that will be run on worker nodes after common setup.
    worker_start_ray_commands: List[str] = field(
        default_factory=lambda: [
            "ray stop",
            "ulimit -n 65536; ray start --address=$RAY_HEAD_IP:6379 --object-manager-port=8076",
        ]
    )


@dataclass
class RayAWSConf(RayConf):
    cluster: RayClusterConf = RayClusterConf()
    run_env: RayRunEnv = RayRunEnv.auto


@dataclass
class RayAWSLauncherConf:
    _target_: str = "hydra_plugins.hydra_ray_launcher.ray_aws_launcher.RayAWSLauncher"

    env_setup: EnvSetupConf = EnvSetupConf()

    ray: RayAWSConf = RayAWSConf()

    # Stop Ray AWS cluster after jobs are finished.
    # (if False, cluster will remain provisioned and can be started with "ray up cluster.yaml").
    stop_cluster: bool = True

    # sync_up is executed before launching jobs on the cluster.
    # This can be used for syncing up source code to remote cluster for execution.
    # You need to sync up if your code contains multiple modules.
    # source is local dir, target is remote dir
    sync_up: RsyncConf = RsyncConf()

    # sync_down is executed after jobs finishes on the cluster.
    # This can be used to download jobs output to local machine avoid the hassle to log on remote machine.
    # source is remote dir, target is local dir
    sync_down: RsyncConf = RsyncConf()


config_store = ConfigStore.instance()
config_store.store(
    group="hydra/launcher",
    name="ray",
    node=RayLauncherConf,
    provider="ray_launcher",
)
config_store.store(
    group="hydra/launcher",
    name="ray_aws",
    node=RayAWSLauncherConf,
    provider="ray_launcher",
)
