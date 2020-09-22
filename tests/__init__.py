# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any, List, Tuple

from omegaconf import MISSING

from hydra.types import TargetConf


def verify_hydra_pytest_plugin_not_installed() -> None:
    try:
        # This check can be removed in 1.1
        import hydra_pytest_plugin  # type: ignore

    except ImportError:
        hydra_pytest_plugin = None

    if hydra_pytest_plugin is not None:
        raise ValueError("hydra-pytest-plugin is no longer required, please uninstall")


verify_hydra_pytest_plugin_not_installed()


def module_function(x: int) -> int:
    return x


@dataclass
class AClass:
    a: Any
    b: Any
    c: Any
    d: Any = "default_value"

    @staticmethod
    def static_method(z: int) -> int:
        return z


@dataclass
class UntypedPassthroughConf:
    _target_: str = "tests.UntypedPassthroughClass"
    a: Any = MISSING


@dataclass
class UntypedPassthroughClass:
    a: Any


# Type not legal in a config
class IllegalType:
    def __eq__(self, other: Any) -> Any:
        return isinstance(other, IllegalType)


@dataclass
class AnotherClass:
    x: int


class ASubclass(AnotherClass):
    @classmethod
    def class_method(cls, y: int) -> Any:
        return cls(y + 1)

    @staticmethod
    def static_method(z: int) -> int:
        return z


class Parameters:
    def __init__(self, params: List[float]):
        self.params = params


@dataclass
class Adam:
    params: Parameters
    lr: float = 0.001
    betas: Tuple[float, ...] = (0.9, 0.999)
    eps: float = 1e-08
    weight_decay: int = 0
    amsgrad: bool = False


@dataclass
class NestingClass:
    a: ASubclass = ASubclass(10)


nesting = NestingClass()


class ClassWithMissingModule:
    def __init__(self) -> None:
        import some_missing_module  # type: ignore # noqa: F401

        self.x = 1


@dataclass
class AdamConf(TargetConf):
    _target_: str = "tests.Adam"
    lr: float = 0.001
    betas: Tuple[float, ...] = (0.9, 0.999)
    eps: float = 1e-08
    weight_decay: int = 0
    amsgrad: bool = False


@dataclass
class BadAdamConf(TargetConf):
    # Missing str annotation
    _target_ = "tests.Adam"


@dataclass
class User:
    name: str = MISSING
    age: int = MISSING


@dataclass
class UserGroup:
    name: str = MISSING
    users: List[User] = MISSING
