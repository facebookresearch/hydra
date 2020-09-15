# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# Generated by configen, do not edit.
# See https://github.com/facebookresearch/hydra/tree/master/tools/configen
# fmt: off
# isort:skip_file
# flake8: noqa

from dataclasses import dataclass, field
from omegaconf import MISSING
from typing import Optional


@dataclass
class WithStringDefaultConf:
    _target_: str = "tests.test_modules.WithStringDefault"
    no_default: str = MISSING
    default_str: str = "Bond, James Bond"
    none_str: Optional[str] = None
