# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
from typing import Any, Union

from omegaconf._utils import is_dict_annotation, is_list_annotation


def is_type_matching(value: Any, type_: Any) -> bool:
    # Union
    if hasattr(type_, "__origin__") and type_.__origin__ is Union:
        types = list(type_.__args__)
        for idx, t in enumerate(types):
            # for now treat any Dict[X,Y] as dict and any List[X] as list, ignoring element types
            if is_dict_annotation(t):
                t = dict
            elif is_list_annotation(t):
                t = list
            types[idx] = t
        return isinstance(value, tuple(types))
    else:
        primitives = (int, float, bool, str)
        if type_ in primitives:
            return type(value) is type_
        if type_ in (Any, inspect.Signature.empty):
            return True
        return isinstance(value, type_)
