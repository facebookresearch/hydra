# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any

from omegaconf import MISSING

from hydra.core.config_store import ConfigStore


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


s = ConfigStore.instance()
s.store(name="config_without_group", node=ConfigWithoutGroup)
s.store(name="dataset", node={"dataset_yaml": True})
s.store(name="cifar10", node=Cifar10, group="dataset", path="dataset")
s.store(name="imagenet.yaml", node=ImageNet, group="dataset", path="dataset")
s.store(name="adam", node=Adam, group="optimizer", path="optimizer")
s.store(name="nesterov", node=Nesterov, group="optimizer", path="optimizer")
s.store(
    name="nested1", node={"l1_l2_n1": True}, group="level1/level2", path="optimizer"
)

s.store(
    name="nested2", node={"l1_l2_n2": True}, group="level1/level2", path="optimizer"
)
