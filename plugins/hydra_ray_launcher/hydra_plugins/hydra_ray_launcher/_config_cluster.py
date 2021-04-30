# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import _config_auth, _config_node_type, _config_provider


@dataclass
class RayDockerConf:
    """
    This class maps to a Ray Docker config, e.g.:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html
    """

    image: str = ""
    head_image: str = ""
    worker_image: str = ""
    container_name: str = "ray_container"
    pull_before_run: bool = True
    run_options: List[str] = field(default_factory=list)
    head_run_options: List[str] = field(default_factory=list)
    worker_run_options: List[str] = field(default_factory=list)
    disable_automatic_runtime_detection: bool = False
    disable_shm_size_detection: bool = False


@dataclass
class RayClusterConf(_config_node_type.RayMaxWorkersConf):
    """
    This class maps to a Ray cluster config, e.g:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#syntax

    Note that we are inheriting from RayMaxWorkersConf so that
    the value for max_workers is propagated to RayNodeTypeConf's
    max_workers value.
    """

    cluster_name: str = "default"
    upscaling_speed: float = 1.0
    idle_timeout_minutes: int = 5
    docker: Optional[RayDockerConf] = None
    file_mounts: Dict[str, str] = field(default_factory=dict)
    cluster_synced_files: List[str] = field(default_factory=list)
    rsync_exclude: List[str] = field(default_factory=list)
    rsync_filter: List[str] = field(default_factory=list)
    initialization_commands: List[str] = field(default_factory=list)
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
    worker_start_ray_commands: List[str] = field(
        default_factory=lambda: [
            "ray stop",
            "ulimit -n 65536; ray start --address=$RAY_HEAD_IP:6379 --object-manager-port=8076",
        ]
    )


@dataclass
class RayOnPremiseClusterConf(RayClusterConf):
    """
    On premise cluster don't have available_node_types.
    provider config is also different than other cloud clusters.
    """

    provider: _config_provider.RayProviderConf = (
        _config_provider.RayOnPremiseProviderConf()
    )
    auth: _config_auth.RayAuthConf = _config_auth.RayAuthConf()


@dataclass
class RayAWSClusterConf(RayClusterConf):
    """
    Defaults for available_node_types and head_node_type are given here based
    on the full configuration, e.g.:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#full-configuration
    """

    provider: _config_provider.RayProviderConf = _config_provider.RayAWSProviderConf()
    auth: _config_auth.RayAuthConf = _config_auth.RayAuthConf()
    available_node_types: Dict[str, _config_node_type.RayAWSNodeTypeConf] = field(
        default_factory=lambda: {
            "ray_head_default": _config_node_type.RayAWSNodeTypeConf(),
            "ray_worker_default": _config_node_type.RayAWSNodeTypeConf(),
        }
    )
    head_node_type: str = "ray_head_default"
    # the value of a worker_nodes key is a Node Config
    # https://docs.ray.io/en/releases-1.3.0/cluster/config.html#node-config
    worker_nodes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RayAzureClusterConf(RayClusterConf):
    """
    Defaults for available_node_types and head_node_type are given here based
    on the full configuration, e.g.:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#full-configuration
    """

    provider: _config_provider.RayProviderConf = _config_provider.RayAzureProviderConf()
    auth: _config_auth.RayAuthConf = _config_auth.RayAzureAuthConf()
    available_node_types: Dict[str, _config_node_type.RayAzureNodeTypeConf] = field(
        default_factory=lambda: {
            "ray_head_default": _config_node_type.RayAzureNodeTypeConf(),
            "ray_worker_default": _config_node_type.RayAzureNodeTypeConf(),
        }
    )
    head_node_type: str = "ray_head_default"
    # the value of a worker_nodes key is a Node Config
    # https://docs.ray.io/en/releases-1.3.0/cluster/config.html#node-config
    worker_nodes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RayGCPClusterConf(RayClusterConf):
    """
    Defaults for available_node_types and head_node_type are given here based
    on the full configuration, e.g.:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#full-configuration
    """

    provider: _config_provider.RayProviderConf = _config_provider.RayGCPProviderConf()
    auth: _config_auth.RayAuthConf = _config_auth.RayAuthConf()
    available_node_types: Dict[str, _config_node_type.RayGCPNodeTypeConf] = field(
        default_factory=lambda: {
            "ray_head_default": _config_node_type.RayGCPNodeTypeConf(),
            "ray_worker_default": _config_node_type.RayGCPNodeTypeConf(),
        }
    )
    head_node_type: str = "ray_head_default"
    # the value of a worker_nodes key is a Node Config
    # https://docs.ray.io/en/releases-1.3.0/cluster/config.html#node-config
    worker_nodes: Dict[str, Any] = field(default_factory=dict)
