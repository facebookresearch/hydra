# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from importlib import import_module
from typing import Any, Dict, List, Optional

from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf
from pkg_resources import get_distribution


@dataclass
class RayConf:
    init: Dict[str, Any] = field(default_factory=lambda: {"address": None})
    remote: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RayLauncherConf:
    _target_: str = "hydra_plugins.hydra_ray_launcher.ray_launcher.RayLauncher"
    ray: RayConf = RayConf()


def _pkg_version(mdl_name: str) -> Optional[str]:
    mdl = import_module(mdl_name)
    ret = getattr(mdl, "__version__")
    assert ret is None or isinstance(ret, str)
    return ret


OmegaConf.register_new_resolver("ray_pkg_version", _pkg_version)

# Ray AWS config, more info on ray's schema here:
# https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/ray-schema.json


class RayAutoScalingMode(Enum):
    default = "default"
    aggressive = "aggressive"


class RayLoggingStyle(Enum):
    """
    If 'pretty', outputs with formatting and color.
    If 'record', outputs record-style without formatting.
    'auto' defaults to 'pretty', and disables pretty logging
    if stdin is *not* a TTY. Defaults to "auto".
    """

    auto = "auto"
    pretty = "pretty"
    record = "record"


class RayLoggingColorMode(Enum):
    """
    Enables or disables `colorful`. Can be "true", "false", or "auto".
    """

    true = "true"
    false = "false"
    auto = "auto"


class RayLoggingVerbosity(IntEnum):
    """
    Low verbosity will disable `verbose` and `very_verbose` messages.
    """

    minimal = 0
    verbose = 1
    very_verbose = 2
    very_very_verbose = 3


@dataclass
class RayLoggingConf:
    """
    Ray sdk.configure_logging parameters: log_style, color_mode, verbosity
    """

    log_style: RayLoggingStyle = RayLoggingStyle.auto
    color_mode: RayLoggingColorMode = RayLoggingColorMode.auto
    verbosity: int = RayLoggingVerbosity.minimal.value


@dataclass
class RayCreateOrUpdateClusterConf:
    """
    Ray sdk.create_or_update_cluster parameters: no_restart, restart_only, no_config_cache
    """

    # Whether to skip restarting Ray services during the
    # update. This avoids interrupting running jobs and can be used to
    # dynamically adjust autoscaler configuration.
    no_restart: bool = False

    # Whether to skip running setup commands and only
    # restart Ray. This cannot be used with 'no-restart'.
    restart_only: bool = False

    # Whether to disable the config cache and fully
    # resolve all environment settings from the Cloud provider again.
    no_config_cache: bool = False


@dataclass
class RayTeardownClusterConf:
    """
    Ray sdk.teardown parameters: workers_only, keep_min_workers
    """

    # Whether to keep the head node running and only
    # teardown worker nodes.
    workers_only: bool = False

    # Whether to keep min_workers (as specified
    # in the RayClusterConf) still running.
    keep_min_workers: bool = False


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
        default_factory=lambda: {"key_name": "hydra-${oc.env:USER,user}"}
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
            "omegaconf": "${ray_pkg_version:omegaconf}",
            "hydra_core": "${ray_pkg_version:hydra}",
            "ray": "${ray_pkg_version:ray}",
            "cloudpickle": "${ray_pkg_version:cloudpickle}",
            "pickle5": get_distribution("pickle5").version,
            "hydra_ray_launcher": get_distribution("hydra_ray_launcher").version,
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

    # populated automatically
    setup_commands: List[str] = field(default_factory=list)

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

    # Ray sdk.configure_logging parameters: log_style, color_mode, verbosity
    logging: RayLoggingConf = RayLoggingConf()

    # Ray sdk.create_or_update_cluster parameters: no_restart, restart_only, no_config_cache
    create_update_cluster: RayCreateOrUpdateClusterConf = RayCreateOrUpdateClusterConf()

    # Ray sdk.teardown parameters: workers_only, keep_min_workers
    teardown_cluster: RayTeardownClusterConf = RayTeardownClusterConf()


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
