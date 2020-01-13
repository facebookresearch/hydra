# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

from omegaconf import Container


@dataclass
class ConfigResult:
    provider: str
    path: str
    config: Container
