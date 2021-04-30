# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Optional

from omegaconf import MISSING


@dataclass
class RayAuthConf:
    """
    This class maps to a Ray auth config, e.g:
    https://docs.ray.io/en/releases-1.3.0/cluster/config.html#auth
    """

    ssh_user: str = MISSING
    ssh_private_key: Optional[str] = None


@dataclass
class RayAzureAuthConf(RayAuthConf):
    """
    Note that for Azure, both ssh_user and ssh_public_key are required.
    """

    ssh_private_key: str = MISSING
    ssh_public_key: str = MISSING
