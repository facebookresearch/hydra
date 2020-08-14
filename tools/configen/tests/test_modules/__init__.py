# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Union


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
