# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from __future__ import annotations  # type: ignore # noqa: F407

from dataclasses import dataclass
from typing import List, Optional

from omegaconf import MISSING


@dataclass
class User:
    name: str = MISSING
    age: int = MISSING


class LibraryClass:
    """
    Some class from a user library that is incompatible with OmegaConf config
    """

    def __eq__(self, other):
        return isinstance(other, type(self))


class ExampleClass:
    def __init__(
        self,
        no_default: float,
        lst: List[str],
        passthrough_list: List[LibraryClass],
        dataclass_val: List[User],
        def_value: List[str] = [],
        default_str="Bond, James Bond",
        none_str: Optional[str] = None,
    ):
        self.no_default = no_default
        self.lst = lst
        self.passthrough_list = passthrough_list
        self.dataclass_val = dataclass_val
        self.def_value = def_value
        self.default_str: str = default_str
        self.none_str = none_str

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.no_default == other.no_default
            and self.lst == other.lst
            and self.passthrough_list == other.passthrough_list
            and self.dataclass_val == other.dataclass_val
            and self.def_value == other.def_value
            and self.default_str == other.default_str
            and self.none_str == other.none_str
        )
