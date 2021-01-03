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
