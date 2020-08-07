# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
from dataclasses import dataclass, field
from inspect import Signature
from typing import Any, Callable, Dict, List, Optional, Type, Union

# TODO: move function related stuff to internal
from omegaconf._utils import is_dict_annotation, is_list_annotation, type_str

from hydra.core.override_parser.types import QuotedString
from hydra.errors import HydraException


@dataclass
class FunctionCall:
    name: str
    args: List[Any]
    kwargs: Dict[str, Any]


def get_list_element_type(ref_type: Optional[Type[Any]]) -> Optional[Type[Any]]:
    args = getattr(ref_type, "__args__", None)
    if ref_type is not List and args is not None and args[0] is not Any:
        element_type = args[0]
    else:
        element_type = None
    assert element_type is None or issubclass(element_type, type)
    return element_type  # type: ignore


# TODO: move to some utils
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


@dataclass
class Functions:
    definitions: Dict[str, Signature] = field(default_factory=dict)
    functions: Dict[str, Callable[..., Any]] = field(default_factory=dict)

    def register(self, name: str, func: Callable[..., Any]) -> None:
        if name in self.definitions:
            raise HydraException(f"Function named '{name}' is already registered")

        self.definitions[name] = inspect.signature(func)
        self.functions[name] = func

    def eval(self, func: FunctionCall) -> Any:
        if func.name not in self.definitions:
            raise HydraException(
                f"Unknown function '{func.name}'"
                f"\nAvailable: {','.join(sorted(self.definitions.keys()))}\n"
            )
        sig = self.definitions[func.name]

        # unquote strings in args
        args = []
        for arg in func.args:
            if isinstance(arg, QuotedString):
                arg = arg.text
            args.append(arg)

        # Unquote strings in kwargs values
        kwargs = {}
        for key, val in func.kwargs.items():
            if isinstance(val, QuotedString):
                val = val.text
            kwargs[key] = val

        bound = sig.bind(*args, **kwargs)

        for idx, arg in enumerate(bound.arguments.items()):
            name = arg[0]
            value = arg[1]
            expected_type = sig.parameters[name].annotation
            if sig.parameters[name].kind == inspect.Parameter.VAR_POSITIONAL:
                for iidx, v in enumerate(value):
                    if not is_type_matching(v, expected_type):
                        raise TypeError(
                            f"mismatch type argument {name}[{iidx}]:"
                            f" {type_str(type(v))} is incompatible with {type_str(expected_type)}"
                        )

            else:
                if not is_type_matching(value, expected_type):
                    raise TypeError(
                        f"mismatch type argument {name}:"
                        f" {type_str(type(value))} is incompatible with {type_str(expected_type)}"
                    )

        bound_args = bound.args
        bound_kwargs = bound.kwargs
        return self.functions[func.name](*bound_args, **bound_kwargs)
