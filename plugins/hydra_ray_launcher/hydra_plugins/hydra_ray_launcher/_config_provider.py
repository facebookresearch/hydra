# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import List

from omegaconf import MISSING


@dataclass
class RayProviderConf:
    """
    This class maps to a Ray Provider config, e.g:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#provider
    """

    type: str = "local"


@dataclass
class RayOnPremiseProviderConf(RayProviderConf):
    """
    head_ip: YOUR_HEAD_NODE_HOSTNAME
    worker_ips: [WORKER_NODE_1_HOSTNAME, WORKER_NODE_2_HOSTNAME, ... ]
    """

    head_ip: str = MISSING
    worker_ips: List[str] = MISSING


@dataclass
class RayAWSProviderConf(RayProviderConf):
    type: str = "aws"
    region: str = "us-west-2"
    availability_zone: str = "us-west-2a,us-west-2b"
    cache_stopped_nodes: bool = False


@dataclass
class RayAzureProviderConf(RayProviderConf):
    type: str = "azure"
    location: str = "westus2"
    resource_group: str = "ray-cluster"
    subscription_id: str = ""
    cache_stopped_nodes: bool = False


@dataclass
class RayGCPProviderConf(RayProviderConf):
    type: str = "gcp"
    region: str = "us-west1"
    availability_zone: str = "us-west1-a"
    project_id: str = "null"
    cache_stopped_nodes: bool = False
