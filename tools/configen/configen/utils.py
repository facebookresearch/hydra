# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys
from collections import defaultdict
from enum import Enum
from typing import Any, List, Optional, Set, Tuple, Type, get_args, get_origin

from omegaconf._utils import _resolve_optional, is_primitive_type


# borrowed from OmegaConf
def type_str(t: Any) -> str:
    is_optional, t = _resolve_optional(t)
    if t is None:
        return type(t).__name__
    if t is Any:
        return "Any"
    if t is ...:
        return "..."

    if sys.version_info < (3, 7, 0):  # pragma: no cover
        # Python 3.6
        if hasattr(t, "__name__"):
            name = str(t.__name__)
        else:
            if t.__origin__ is not None:
                name = type_str(t.__origin__)
            else:
                name = str(t)
                if name.startswith("typing."):
                    name = name[len("typing.") :]
    else:  # pragma: no cover
        # Python >= 3.7
        if hasattr(t, "__name__"):
            name = str(t.__name__)
        else:
            if t._name is None:
                if get_origin(t) is not None:
                    name = type_str(t.__origin__)
            else:
                name = str(t._name)

    args = get_args(t) if hasattr(t, "__args__") else None
    if args is not None:
        args = ", ".join([type_str(t) for t in (list(args))])
        ret = f"{name}[{args}]"
    else:
        ret = name
    if is_optional:
        return f"Optional[{ret}]"
    else:
        return ret


def is_tuple_annotation(type_: Any) -> bool:
    origin = getattr(type_, "__origin__", None)
    if sys.version_info < (3, 7, 0):
        return origin is Tuple or type_ is Tuple  # pragma: no cover
    else:
        return origin is tuple  # pragma: no cover


def convert_imports(imports: Set[Type], string_imports: Set[str]) -> List[str]:
    tmp = set()
    for import_ in imports:
        origin = getattr(import_, "__origin__", None)
        if import_ is Any:
            classname = "Any"
        elif import_ is Optional:
            classname = "Optional"
        else:
            if origin is list:
                classname = "List"
            elif origin is tuple:
                classname = "Tuple"
            elif origin is dict:
                classname = "Dict"
            else:
                classname = import_.__name__
        if not is_primitive_type(import_) or issubclass(import_, Enum):
            tmp.add(f"from {import_.__module__} import {classname}")

    return sorted(list(tmp.union(string_imports)))


def collect_imports(imports: Set[Type], type_: Type) -> None:
    for arg in get_args(type_):
        if arg is not ...:
            collect_imports(imports, arg)
    if _resolve_optional(type_)[0] and type_ is not Any:
        type_ = Optional
    imports.add(type_)
