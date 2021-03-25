# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import sys
from enum import Enum
from typing import Any, Callable, Sequence, Tuple, Union

from omegaconf import OmegaConf, SCMode
from omegaconf._utils import is_structured_config

from hydra._internal.utils import _locate
from hydra.errors import InstantiationException
from hydra.types import ConvertMode, TargetConf


class _Keys(str, Enum):
    """Special keys in configs used by instantiate."""

    TARGET = "_target_"
    CONVERT = "_convert_"
    RECURSIVE = "_recursive_"
    ARGS = "_args_"


def _is_target(x: Any) -> bool:
    if isinstance(x, dict):
        return "_target_" in x
    if OmegaConf.is_dict(x):
        return "_target_" in x
    return False


def _extract_pos_args(*input_args: Any, **kwargs: Any) -> Tuple[Any, Any]:
    config_args = kwargs.pop(_Keys.ARGS, ())
    output_args = config_args

    if isinstance(config_args, Sequence):
        if len(input_args) > 0:
            output_args = input_args
    else:
        raise InstantiationException(
            f"Unsupported _args_ type: {type(config_args).__name__}. value: {config_args}"
        )

    return output_args, kwargs


def _call_target(target: Callable, *args, **kwargs) -> Any:  # type: ignore
    """Call target (type) with args and kwargs."""
    try:
        args, kwargs = _extract_pos_args(*args, **kwargs)
        # detaching configs from parent.
        # At this time, everything is resolved and the parent link can cause
        # issues when serializing objects in some scenarios.
        for arg in args:
            if OmegaConf.is_config(arg):
                arg._set_parent(None)
        for v in kwargs.values():
            if OmegaConf.is_config(v):
                v._set_parent(None)

        return target(*args, **kwargs)
    except Exception as e:
        raise type(e)(
            f"Error instantiating '{_convert_target_to_string(target)}' : {e}"
        ).with_traceback(sys.exc_info()[2])


def _convert_target_to_string(t: Any) -> Any:
    if isinstance(t, type):
        return f"{t.__module__}.{t.__name__}"
    elif callable(t):
        return f"{t.__module__}.{t.__qualname__}"
    else:
        return t


def _prepare_input_dict(d: Any) -> Any:
    res: Any
    if isinstance(d, dict):
        res = {}
        for k, v in d.items():
            if k == "_target_":
                v = _convert_target_to_string(d["_target_"])
            elif isinstance(v, (dict, list)):
                v = _prepare_input_dict(v)
            res[k] = v
    elif isinstance(d, list):
        res = []
        for v in d:
            if isinstance(v, (list, dict)):
                v = _prepare_input_dict(v)
            res.append(v)
    else:
        assert False
    return res


def _resolve_target(
    target: Union[str, type, Callable[..., Any]]
) -> Union[type, Callable[..., Any]]:
    """Resolve target string, type or callable into type or callable."""
    if isinstance(target, str):
        return _locate(target)
    if isinstance(target, type):
        return target
    if callable(target):
        return target
    raise InstantiationException(
        f"Unsupported target type: {type(target).__name__}. value: {target}"
    )


def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An config object describing what to call and what params to use.
                   In addition to the parameters, the config must contain:
                   _target_ : target class or callable name (str)
                   And may contain:
                   _args_: List-like of positional arguments to pass to the target
                   _recursive_: Construct nested objects as well (bool).
                                True by default.
                                may be overridden via a _recursive_ key in
                                the kwargs
                   _convert_: Conversion strategy
                        none    : Passed objects are DictConfig and ListConfig, default
                        partial : Passed objects are converted to dict and list, with
                                  the exception of Structured Configs (and their fields).
                        all     : Passed objects are dicts, lists and primitives without
                                  a trace of OmegaConf containers
                   _args_: List-like of positional arguments
    :param args: Optional positional parameters pass-through
    :param kwargs: Optional named parameters to override
                   parameters in the config object. Parameters not present
                   in the config objects are being passed as is to the target.
                   IMPORTANT: dataclasses instances in kwargs are interpreted as config
                              and cannot be used as passthrough
    :return: if _target_ is a class name: the instantiated object
             if _target_ is a callable: the return value of the call
    """

    # Return None if config is None
    if config is None:
        return None

    # TargetConf edge case
    if isinstance(config, TargetConf) and config._target_ == "???":
        # Specific check to give a good warning about failure to annotate _target_ as a string.
        raise InstantiationException(
            f"Missing value for {type(config).__name__}._target_. Check that it's properly annotated and overridden."
            f"\nA common problem is forgetting to annotate _target_ as a string : '_target_: str = ...'"
        )

    if isinstance(config, dict):
        config = _prepare_input_dict(config)

    kwargs = _prepare_input_dict(kwargs)

    # Structured Config always converted first to OmegaConf
    if is_structured_config(config) or isinstance(config, dict):
        config = OmegaConf.structured(config, flags={"allow_objects": True})

    if OmegaConf.is_dict(config):
        # Finalize config (convert targets to strings, merge with kwargs)
        config_copy = copy.deepcopy(config)
        config_copy._set_flag(
            flags=["allow_objects", "struct", "readonly"], values=[True, False, False]
        )
        config_copy._set_parent(config._get_parent())
        config = config_copy

        if kwargs:
            config = OmegaConf.merge(config, kwargs)

        OmegaConf.resolve(config)

        _recursive_ = config.pop(_Keys.RECURSIVE, True)
        _convert_ = config.pop(_Keys.CONVERT, ConvertMode.NONE)

        return instantiate_node(config, *args, recursive=_recursive_, convert=_convert_)
    else:
        raise InstantiationException(
            "Top level config has to be OmegaConf DictConfig, plain dict, or a Structured Config class or instance"
        )


def _convert_node(node: Any, convert: Union[ConvertMode, str]) -> Any:
    if OmegaConf.is_config(node):
        if convert == ConvertMode.ALL:
            node = OmegaConf.to_container(node, resolve=True)
        elif convert == ConvertMode.PARTIAL:
            node = OmegaConf.to_container(
                node, resolve=True, structured_config_mode=SCMode.DICT_CONFIG
            )
    return node


def instantiate_node(
    node: Any,
    *args: Any,
    convert: Union[str, ConvertMode] = ConvertMode.NONE,
    recursive: bool = True,
) -> Any:
    # Return None if config is None
    if node is None or (OmegaConf.is_config(node) and node._is_none()):
        return None

    if not OmegaConf.is_config(node):
        return node

    # Override parent modes from config if specified
    if OmegaConf.is_dict(node):
        # using getitem instead of get(key, default) because OmegaConf will raise an exception
        # if the key type is incompatible on get.
        convert = node[_Keys.CONVERT] if _Keys.CONVERT in node else convert
        recursive = node[_Keys.RECURSIVE] if _Keys.RECURSIVE in node else recursive

    if not isinstance(recursive, bool):
        raise TypeError(f"_recursive_ flag must be a bool, got {type(recursive)}")

    # If OmegaConf list, create new list of instances if recursive
    if OmegaConf.is_list(node):
        items = [
            instantiate_node(item, convert=convert, recursive=recursive)
            for item in node._iter_ex(resolve=True)
        ]

        if convert in (ConvertMode.ALL, ConvertMode.PARTIAL):
            # If ALL or PARTIAL, use plain list as container
            return items
        else:
            # Otherwise, use ListConfig as container
            lst = OmegaConf.create(items, flags={"allow_objects": True})
            lst._set_parent(node)
            return lst

    elif OmegaConf.is_dict(node):
        exclude_keys = set({"_target_", "_convert_", "_recursive_"})
        if _is_target(node):
            target = _resolve_target(node.get(_Keys.TARGET))
            kwargs = {}
            for key, value in node.items():
                if key not in exclude_keys:
                    if recursive:
                        value = instantiate_node(
                            value, convert=convert, recursive=recursive
                        )
                    kwargs[key] = _convert_node(value, convert)
            return _call_target(target, *args, **kwargs)
        else:
            # If ALL or PARTIAL non structured, instantiate in dict and resolve interpolations eagerly.
            if convert == ConvertMode.ALL or (
                convert == ConvertMode.PARTIAL and node._metadata.object_type is None
            ):
                dict_items = {}
                for key, value in node.items():
                    # list items inherits recursive flag from the containing dict.
                    dict_items[key] = instantiate_node(
                        value, convert=convert, recursive=recursive
                    )
                return dict_items
            else:
                # Otherwise use DictConfig and resolve interpolations lazily.
                cfg = OmegaConf.create({}, flags={"allow_objects": True})
                for key, value in node.items():
                    cfg[key] = instantiate_node(
                        value, convert=convert, recursive=recursive
                    )
                cfg._set_parent(node)
                cfg._metadata.object_type = node._metadata.object_type
                return cfg

    else:
        assert False, f"Unexpected config type : {type(node).__name__}"
