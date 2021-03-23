# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from omegaconf import MISSING


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


@dataclass
class User:
    name: str = MISSING
    age: int = MISSING


class LibraryClass:
    """
    Some class from a user library that is incompatible with OmegaConf config
    """

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, type(self))


class WithStringDefault:
    def __init__(
        self,
        no_default: str,
        default_str: str = "Bond, James Bond",
        none_str: Optional[str] = None,
    ):
        self.no_default = no_default
        self.default_str = default_str
        self.none_str = none_str

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.no_default == other.no_default
            and self.default_str == other.default_str
            and self.none_str == other.none_str
        )


class WithUntypedStringDefault:
    def __init__(
        self,
        default_str="Bond, James Bond",
    ):
        self.default_str = default_str

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.default_str == other.default_str


class ListValues:
    def __init__(
        self,
        lst: List[str],
        enum_lst: List[Color],
        passthrough_list: List[LibraryClass],
        dataclass_val: List[User],
        def_value: List[str] = [],
    ):
        self.lst = lst
        self.enum_lst = enum_lst
        self.passthrough_list = passthrough_list
        self.dataclass_val = dataclass_val
        self.def_value = def_value

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.lst == other.lst
            and self.enum_lst == other.enum_lst
            and self.passthrough_list == other.passthrough_list
            and self.dataclass_val == other.dataclass_val
            and self.def_value == other.def_value
        )
