# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import sys
from enum import Enum
from typing import Any, Callable, Union

from omegaconf import Container, OmegaConf
from omegaconf._utils import is_structured_config

from hydra._internal.utils import _locate
from hydra.errors import InstantiationException
from hydra.types import ConvertMode, TargetConf


class _Keys(str, Enum):
    """Special keys in configs used by instantiate."""

    TARGET = "_target_"
    CONVERT = "_convert_"
    RECURSIVE = "_recursive_"


def _is_target(x: Any) -> bool:
    if isinstance(x, dict):
        return "_target_" in x
    if OmegaConf.is_dict(x) and not OmegaConf.is_none(x):
        return "_target_" in x
    return False


def _call_target(target: Callable, *args, **kwargs) -> Any:  # type: ignore
    """Call target (type) with args and kwargs."""
    try:
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


def _convert_container_targets_to_strings(d: Any) -> None:
    if isinstance(d, dict):
        if "_target_" in d:
            d["_target_"] = _convert_target_to_string(d["_target_"])
        for _, v in d.items():
            _convert_container_targets_to_strings(v)
    elif isinstance(d, list):
        for e in d:
            if isinstance(e, (list, dict)):
                _convert_container_targets_to_strings(e)


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
        f"Unsupported target type : {type(target)} (target = {target})"
    )


def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An config object describing what to call and what params to use.
                   In addition to the parameters, the config must contain:
                   _target_ : target class or callable name (str)
                   And may contain:
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
    if config is None or OmegaConf.is_none(config):
        return None

    # TargetConf edge case
    if isinstance(config, TargetConf) and config._target_ == "???":
        # Specific check to give a good warning about failure to annotate _target_ as a string.
        raise InstantiationException(
            f"Missing value for {type(config).__name__}._target_. Check that it's properly annotated and overridden."
            f"\nA common problem is forgetting to annotate _target_ as a string : '_target_: str = ...'"
        )

    _convert_container_targets_to_strings(config)
    _convert_container_targets_to_strings(kwargs)

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

        _recursive_ = config.pop(_Keys.RECURSIVE, True)
        _convert_ = config.pop(_Keys.CONVERT, ConvertMode.NONE)

        return instantiate_node(config, *args, recursive=_recursive_, convert=_convert_)
    else:
        raise InstantiationException(
            "Top level config has to be OmegaConf DictConfig, plain dict, or a Structured Config class or instance"
        )


def _convert_conf(config: Container, convert: Union[ConvertMode, str]) -> Any:
    if convert == ConvertMode.ALL:
        return OmegaConf.to_container(config, resolve=True)
    if convert == ConvertMode.PARTIAL:
        return OmegaConf.to_container(
            config, resolve=True, exclude_structured_configs=True
        )
    else:
        return config


def instantiate_node(
    config: Any,
    *args: Any,
    convert: Union[str, ConvertMode] = ConvertMode.NONE,
    recursive: bool = True,
) -> Any:
    # Return None if config is None
    if config is None or OmegaConf.is_none(config):
        return None

    if OmegaConf.is_config(config):
        # Turn off struct flag on node to enable popping fields from Structured Configs.
        OmegaConf.set_struct(config, False)
    else:
        # probably a primitive node, return as is.
        return config

    # Override parent modes from config if specified
    if OmegaConf.is_dict(config):
        convert = config.pop(_Keys.CONVERT) if _Keys.CONVERT in config else convert
        recursive = (
            config.pop(_Keys.RECURSIVE) if _Keys.RECURSIVE in config else recursive
        )
        if not isinstance(recursive, bool):
            raise TypeError(f"_recursive_ flag must be a bool, got {type(recursive)}")

    # If OmegaConf list, create new list of instances if recursive
    if OmegaConf.is_list(config):
        if recursive:
            items = [
                instantiate_node(item, convert=convert, recursive=recursive)
                for item in config._iter_ex(resolve=True)
            ]

            if convert in (ConvertMode.ALL, ConvertMode.PARTIAL):
                # If ALL or PARTIAL, use plain list as container
                return items
            else:
                # Otherwise, use ListConfig as container
                lst = OmegaConf.create(items, flags={"allow_objects": True})
                lst._set_parent(config)
                return lst
        else:
            return _convert_conf(config, convert)

    elif OmegaConf.is_dict(config):
        if _is_target(config):
            target = _resolve_target(config.pop(_Keys.TARGET))
            if recursive:
                final_kwargs = {}
                for key, value in config.items_ex(resolve=True):
                    final_kwargs[key] = instantiate_node(
                        value, convert=convert, recursive=recursive
                    )
            else:
                final_kwargs = config
            return _call_target(target, *args, **final_kwargs)

        if recursive:
            # If ALL or PARTIAL non structured, instantiate in dict and resolve interpolations eagerly.
            if convert == ConvertMode.ALL or (
                convert == ConvertMode.PARTIAL and config._metadata.object_type is None
            ):
                dict_items = {}
                for key, value in config.items_ex(resolve=True):
                    dict_items[key] = instantiate_node(
                        value, convert=convert, recursive=recursive
                    )
                return dict_items
            else:
                # Otherwise use DictConfig and resolve interpolations lazily.
                cfg = OmegaConf.create({}, flags={"allow_objects": True})
                for key, value in config.items_ex(resolve=False):
                    cfg[key] = instantiate_node(
                        value, convert=convert, recursive=recursive
                    )
                cfg._set_parent(config)
                cfg._metadata.object_type = config._metadata.object_type
                return cfg
        else:
            return _convert_conf(config, convert)

    else:
        assert False, f"Unexpected config type : {type(config).__name__}"
