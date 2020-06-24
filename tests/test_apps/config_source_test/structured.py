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
s.store(group="dataset", name="cifar10", node=Cifar10)
s.store(group="dataset", name="imagenet.yaml", node=ImageNet)
s.store(group="optimizer", name="adam", node=Adam)
s.store(group="optimizer", name="nesterov", node=Nesterov)
s.store(
    group="level1/level2", name="nested1", node={"l1_l2_n1": True}, package="_global_"
)
s.store(
    group="level1/level2", name="nested2", node={"l1_l2_n2": True}, package="_global_"
)
s.store(group="package_test", name="none", node={"foo": "bar"}, package="_global_")
s.store(group="package_test", name="explicit", node={"foo": "bar"}, package="a.b")
s.store(group="package_test", name="global", node={"foo": "bar"}, package="_global_")
s.store(group="package_test", name="group", node={"foo": "bar"}, package="_group_")
s.store(
    group="package_test",
    name="group_name",
    node={"foo": "bar"},
    package="foo._group_._name_",
)
s.store(group="package_test", name="name", node={"foo": "bar"}, package="_name_")
s.store(name="primary_config", node={"primary": True}, package=None)
s.store(
    name="primary_config_with_non_global_package", node={"primary": True}, package="foo"
)
