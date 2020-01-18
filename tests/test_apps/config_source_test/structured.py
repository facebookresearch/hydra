# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any

from omegaconf import MISSING

from hydra.core.structured_config_store import StructuredConfigStore


@dataclass
class ConfigWithoutGroup:
    group: bool = False


@dataclass
class Cifar10:
    name: str = "cifar10"
    path: str = "/datasets/cifar10"


@dataclass
class ImageNet:
    name: str = "imagenet"
    path: str = "/datasets/imagenet"


@dataclass
class ConfigWithoutExt:
    foo: str = "bar"


@dataclass
class Adam:
    type: str = "adam"
    lr: float = 0.1
    beta: float = 0.01


@dataclass
class Nesterov:
    type: str = "nesterov"
    lr: float = 0.001


@dataclass
class Optimizer:
    optimizer: Any = MISSING


s = StructuredConfigStore.instance()
s.store(group=None, name="config_without_group", path="", node=ConfigWithoutGroup)
s.store(group=None, name="dataset", path=None, node={"dataset_yaml": True})
s.store(
    group="dataset", name="cifar10", path="dataset", node=Cifar10,
)
s.store(group="dataset", name="imagenet", path="dataset", node=ImageNet)
s.store(group="optimizer", name="adam", path="optimizer", node=Adam)
s.store(group="optimizer", name="nesterov", path="optimizer", node=Nesterov)
s.store(
    group="level1/level2", name="nested1", path="optimizer", node={"l1_l2_n1": True},
)

s.store(
    group="level1/level2", name="nested2", path="optimizer", node={"l1_l2_n2": True},
)
