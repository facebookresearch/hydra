# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from omegaconf import MISSING

TaskFunction = Callable[[Any], Any]


@dataclass
class TargetConf:
    """
    This class is going away in Hydra 1.2.
    You should no longer extend it or annotate with it.
    instantiate will work correctly if you pass in a DictConfig object or any dataclass that has the
    _target_ attribute.
    """

    _target_: str = MISSING

    def __post_init__(self) -> None:
        # DEPRECATED: remove in 1.2
        msg = "\nTargetConf is deprecated since Hydra 1.1 and will be removed in Hydra 1.2."
        warnings.warn(message=msg, category=UserWarning)


class RunMode(Enum):
    RUN = 1
    MULTIRUN = 2


class ConvertMode(str, Enum):
    """ConvertMode for instantiate, controls return type.

    A config is either config or instance-like (`_target_` field).

    If instance-like, instantiate resolves the callable (class or
    function) and returns the result of the call on the rest of the
    parameters.

    If "none", config-like configs will be kept as is.

    If "partial", config-like configs will be converted to native python
    containers (list and dict), unless they are structured configs (
    dataclasses or attr instances).

    If "all", config-like configs will all be converted to native python
    containers (list and dict).
    """

    # Use DictConfig/ListConfig
    NONE = "none"
    # Convert the OmegaConf config to primitive container, Structured Configs are preserved
    PARTIAL = "partial"
    # Fully convert the OmegaConf config to primitive containers (dict, list and primitives).
    ALL = "all"
