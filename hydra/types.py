# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict

from omegaconf import MISSING

TaskFunction = Callable[[Any], Any]


@dataclass
# This extends Dict[str, Any] to allow for the deprecated "class" field.
# Once support for class field removed this can stop extending Dict.
class ObjectConf(Dict[str, Any]):
    def __post_init__(self) -> None:
        msg = (
            "\nObjectConf is deprecated in favor of TargetConf since Hydra 1.0.0rc3 and will be removed in Hydra 1.1."
            "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
        )
        warnings.warn(message=msg, category=UserWarning)

    # class, class method or function name
    target: str = MISSING

    # parameters to pass to cls when calling it
    params: Any = field(default_factory=dict)


@dataclass
class TargetConf:
    """
    Use by subclassing and adding fields
    e.g:
    @dataclass
    class UserConf:
        _target_ : str = "module.User"
        name: str = MISSING
        age: int = MISSING
    """

    # class, class method or function name
    _target_: str = MISSING


class RunMode(Enum):
    RUN = 1
    MULTIRUN = 2
