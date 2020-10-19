# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

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


class Empty:
    def __init__(self):
        ...

    def __eq__(self, other):
        return isinstance(other, type(self))


class UntypedArg:
    def __init__(self, param):
        self.param = param

    def __eq__(self, other):
        return isinstance(other, type(self)) and other.param == self.param


class IntArg:
    def __init__(self, param: int):
        self.param = param

    def __eq__(self, other):
        return isinstance(other, type(self)) and other.param == self.param


class UnionArg:
    # Union is not currently supported by OmegaConf, it will be typed as Any
    def __init__(self, param: Union[int, float]):
        self.param = param

    def __eq__(self, other):
        return isinstance(other, type(self)) and other.param == self.param


class WithLibraryClassArg:
    def __init__(self, num: int, param: LibraryClass):
        self.num = num
        self.param = param

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and other.num == self.num
            and other.param == self.param
        )


@dataclass
class IncompatibleDataclass:
    library: LibraryClass = LibraryClass()

    def __eq__(self, other):
        return isinstance(other, type(self)) and other.library == self.library


class IncompatibleDataclassArg:
    def __init__(self, num: int, incompat: IncompatibleDataclass):
        self.num = num
        self.incompat = incompat

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.num == other.num
            and self.incompat == other.incompat
        )


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


class DictValues:
    def __init__(
        self,
        dct: Dict[str, str],
        enum_key: Dict[Color, str],
        dataclass_val: Dict[str, User],
        passthrough_dict: Dict[str, LibraryClass],
        def_value: Dict[str, str] = {},
    ):
        self.dct = dct
        self.enum_key = enum_key
        self.dataclass_val = dataclass_val
        self.passthrough_dict = passthrough_dict
        self.def_value = def_value

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.dct == other.dct
            and self.enum_key == other.enum_key
            and self.dataclass_val == other.dataclass_val
            and self.passthrough_dict == other.passthrough_dict
            and self.def_value == other.def_value
        )


class PeskySentinel(object):
    def __repr__(self):
        return "<I am a pesky sentinel>"


pesky = PeskySentinel()


class PeskySentinelUsage:
    def __init__(self, foo=pesky):
        self.foo = foo

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.foo == other.foo


class Tuples:
    def __init__(
        self,
        t1: Tuple[float, float],
        t2=(1, 2, 3),
        t3: Tuple[float, ...] = (0.1, 0.2, 0.3),
    ):
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.t1 == other.t1
            and self.t2 == other.t2
            and self.t3 == other.t3
        )
