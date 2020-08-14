# Compared against generated code
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# fmt: off
# isort:skip_file
# flake8: noqa
from dataclasses import dataclass
from typing import *

from hydra.types import ObjectConf
from omegaconf import MISSING


@dataclass
class IncompatibleDataclassArgParams:
    num: int = MISSING
    # [passthrough] incompat: Incompatible


@dataclass
class IncompatibleDataclassArgConf(ObjectConf):
    target: str = "tests.test_modules.IncompatibleDataclassArg"
    params: IncompatibleDataclassArgParams = MISSING
