# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RayMaxWorkersConf:
    max_workers: int = 1


@dataclass
class RayResourcesConf:
    """
    This class maps to a Ray Resource config, e.g:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#resources
    """

    CPU: int = 2
    GPU: int = 0


@dataclass
class RayNodeTypeConf(RayMaxWorkersConf):
    """
    This class maps to a Ray Node Type config, e.g:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#node-types
    """

    resources: RayResourcesConf = RayResourcesConf()
    min_workers: int = 0
    worker_setup_commands: List[str] = field(default_factory=list)
    docker: Dict[str, str] = field(default_factory=dict)


@dataclass
class RayAWSNodeTypeConf(RayNodeTypeConf):
    """
    Note that more configuration options are available, check:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#node-config
    """

    node_config: Dict[Any, Any] = field(
        default_factory=lambda: {
            "InstanceType": "m5.large",
            "ImageId": "ami-008d8ed4bd7dc2485",
        }
    )


@dataclass
class RayAzureNodeTypeConf(RayNodeTypeConf):
    """
    Note that more configuration options are available, check:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#node-config
    """

    node_config: Dict[Any, Any] = field(
        default_factory=lambda: {
            "azure_arm_parameters": {
                "vmSize": "Standard_D2s_v3",
                "imagePublisher": "microsoft-dsvm",
                "imageOffer": "ubuntu-1804",
                "imageSku": "1804-gen2",
                "imageVersion": "20.07.06",
            }
        }
    )


@dataclass
class RayGCPNodeTypeConf(RayNodeTypeConf):
    """
    Note that more configuration options are available, check:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#node-config
    """

    node_config: Dict[Any, Any] = field(
        default_factory=lambda: {
            "machineType": "n1-standard-2",
            "disks": [
                {
                    "boot": True,
                    "autoDelete": True,
                    "type": "PERSISTENT",
                    "initializeParams": {
                        "diskSizeGb": 50,
                        "sourceImage": "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20201014",
                    },
                }
            ],
            # Ray doesn't support OS login at the moment
            "metadata": {
                "items": [
                    {
                        "key": "enable-oslogin",
                        "value": "FALSE"
                    }
                ]
            }
        }
    )
