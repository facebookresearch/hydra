# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union

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


class Empty:
    def __init__(self):
        ...


class UntypedArg:
    def __init__(self, param):
        ...


class IntArg:
    def __init__(self, param: int):
        ...


class UnionArg:
    # Union is not currently supported by OmegaConf, it will be typed as Any
    def __init__(self, param: Union[int, float]):
        ...


class WithLibraryClassArg:
    def __init__(self, num: int, param: LibraryClass):
        ...


@dataclass
class Incompatible:
    library: LibraryClass = LibraryClass()


class IncompatibleDataclassArg:
    def __init__(self, num: int, incompat: Incompatible):
        ...


class WithStringDefault:
    def __init__(
        self,
        no_default: str,
        default_str: str = "Bond, James Bond",
        none_str: Optional[str] = None,
    ):
        ...


class ListValues:
    def __init__(
        self,
        lst: List[str],
        enum_lst: List[Color],
        passthrough_list: List[LibraryClass],
        dataclass_val: List[User],
        def_value: List[str] = [],
    ):
        ...


class DictValues:
    def __init__(
        self,
        dct: Dict[str, str],
        enum_key: Dict[Color, str],
        dataclass_val: Dict[str, User],
        passthrough_dict: Dict[str, LibraryClass],
        def_value: Dict[str, str] = {},
    ):
        ...
