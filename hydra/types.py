# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Callable, Dict

from omegaconf import MISSING

TaskFunction = Callable[[Any], Any]


@dataclass
# This extends Dict[str, Any] to allow for the deprecated "class" field.
# Once support for class field removed this can stop extending Dict.
class ObjectConf(Dict[str, Any]):
    # class, class method or function name
    cls: str = MISSING
    # parameters to pass to cls when calling it
    params: Any = field(default_factory=dict)
