# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from enum import Enum
from importlib import import_module
from typing import Any, Dict, List, Optional

from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf
from pkg_resources import get_distribution

from . import _config_cluster


def _pkg_version(mdl_name: str) -> Optional[str]:
    mdl = import_module(mdl_name)
    ret = getattr(mdl, "__version__")
    assert ret is None or isinstance(ret, str)
    return ret


OmegaConf.register_new_resolver("ray_pkg_version", _pkg_version)


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
            "hydra_core": "1.1.0dev5",
            "ray": "${ray_pkg_version:ray}",
            "cloudpickle": "${ray_pkg_version:cloudpickle}",
            "pickle5": get_distribution("pickle5").version,
            "hydra_ray_launcher": get_distribution("hydra_ray_launcher").version,
            "hydra_joblib_launcher": "1.1.5.dev1",
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
class RayConf:
    init: Dict[str, Any] = field(default_factory=lambda: {"address": None})
    remote: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RayAutoscalerConf(RayConf):
    run_env: RayRunEnv = RayRunEnv.auto


@dataclass
class RayOnPremiseAutoscalerConf(RayAutoscalerConf):
    cluster: _config_cluster.RayClusterConf = _config_cluster.RayOnPremiseClusterConf()


@dataclass
class RayAWSAutoscalerConf(RayAutoscalerConf):
    cluster: _config_cluster.RayClusterConf = _config_cluster.RayAWSClusterConf()


@dataclass
class RayAzureAutoscalerConf(RayAutoscalerConf):
    cluster: _config_cluster.RayClusterConf = _config_cluster.RayAzureClusterConf()


@dataclass
class RayGCPAutoscalerConf(RayAutoscalerConf):
    cluster: _config_cluster.RayClusterConf = _config_cluster.RayGCPClusterConf()


@dataclass
class RayLauncherConf:
    _target_: str = "hydra_plugins.hydra_ray_launcher.ray_launcher.RayLauncher"
    ray: RayConf = RayConf()


@dataclass
class RayAutoscalerLauncherConf(RayLauncherConf):
    _target_: str = (
        "hydra_plugins.hydra_ray_launcher.ray_autoscaler_launcher.RayAutoScalerLauncher"
    )

    env_setup: EnvSetupConf = EnvSetupConf()

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

    no_restart: bool = False
    restart_only: bool = False
    no_config_cache: bool = False


@dataclass
class RayOnPremiseAutoscalerLauncherConf(RayAutoscalerLauncherConf):
    ray: RayAutoscalerConf = RayOnPremiseAutoscalerConf()


@dataclass
class RayAWSAutoscalerLauncherConf(RayAutoscalerLauncherConf):
    ray: RayAutoscalerConf = RayAWSAutoscalerConf()


@dataclass
class RayAzureAutoscalerLauncherConf(RayAutoscalerLauncherConf):
    ray: RayAutoscalerConf = RayAzureAutoscalerConf()


@dataclass
class RayGCPAutoscalerLauncherConf(RayAutoscalerLauncherConf):
    ray: RayAutoscalerConf = RayGCPAutoscalerConf()


config_store = ConfigStore.instance()
config_store.store(
    group="hydra/launcher",
    name="ray",
    node=RayLauncherConf,
    provider="ray_launcher",
)
config_store.store(
    group="hydra/launcher",
    name="ray_on_premise",
    node=RayOnPremiseAutoscalerLauncherConf,
    provider="ray_autoscaler_launcher",
)
config_store.store(
    group="hydra/launcher",
    name="ray_aws",
    node=RayAWSAutoscalerLauncherConf,
    provider="ray_autoscaler_launcher",
)
config_store.store(
    group="hydra/launcher",
    name="ray_azure",
    node=RayAzureAutoscalerLauncherConf,
    provider="ray_autoscaler_launcher",
)
config_store.store(
    group="hydra/launcher",
    name="ray_gcp",
    node=RayGCPAutoscalerLauncherConf,
    provider="ray_autoscaler_launcher",
)
