# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging.config
import os
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Union

from omegaconf import OmegaConf
from omegaconf._utils import is_structured_config

from hydra._internal.utils import (
    _call_target,
    _convert_container_targets_to_strings,
    _is_target,
    _Keys,
    _locate,
    _merge_overrides_into_config,
    _resolve_target,
)
from hydra.core.hydra_config import HydraConfig
from hydra.errors import InstantiationException
from hydra.types import TargetConf

log = logging.getLogger(__name__)


class ConvertMode(str, Enum):
    """ConvertMode for instantiate, controls return type.

    A config is either config or instance-like (`_target_` field).

    If instance-like, instantiate resolves the callable (class or
    function) and returns the result of the call on the rest of the
    parameters.

    If "none", config-like configs will be kept as is.

    If "partial", config-like configs will be converted to native python
    containers (list and dict), unless they are structured configs (
    dataclasses or attr instances).

    If "all", config-like configs will all be converted to native python
    containers (list and dict).
    """

    # Use DictConfig/ListConfig
    NONE = "none"
    # Convert the OmegaConf config to primitive container, Structured Configs are preserved
    PARTIAL = "partial"
    # Fully convert the OmegaConf config to primitive containers (dict, list and primitives).
    ALL = "all"


class ParseMode(str, Enum):
    """ParseMode for instantiate, controls input type.

    If the config is a native python dictionary (no trace of OmegaConf
    containers), it is automatically converted to an OmegaConf container
    during instantiate. This is the expected behavior, since the
    interpolation syntax might be used in the native python dictionary.

    This behavior can be disable with ParseMode.NONE. Please make sure
    the config given to instantiate is fully defined (no interpolation).
    """

    NONE = "none"  # Keep original config type
    NATIVE = "native"  # Convert to dict / list if OmegaConf config
    OMEGACONF = "omegaconf"  # Convert config to OmegaConf container


def instantiate(
    config: Any,
    *args: Any,
    parse: Union[str, ParseMode] = ParseMode.OMEGACONF,
    convert: Union[str, ConvertMode] = ConvertMode.NONE,
    recursive: bool = True,
    **kwargs: Any,
) -> Any:
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
    :param parse: Optional ParseMode or str from parent. Will be used
                  if _parse_ is not set in kwargs or config.
    :param convert: Optional ConvertMode or str from parent. Will be
                    used if _convert_ is not set in kwargs or config.
    :param recursive: Optional bool from parent. Will be used if
                      _recursive is not set in kwargs or config.
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

    # Structured Config always converted first to OmegaConf
    if is_structured_config(config):
        config = OmegaConf.structured(config, flags={"allow_objects": True})

    # Make copy if config is a standard dictionary
    if isinstance(config, dict):

        def _rec_copy(d: Any) -> Any:
            """Copy dictionary and children."""
            if isinstance(d, dict):
                return {key: _rec_copy(value) for key, value in d.items()}
            return d

        config = _rec_copy(config)

    # If OmegaConf, copy, make it mutable and set parent for live interpolation
    if OmegaConf.is_config(config):
        config_copy = OmegaConf.structured(config, flags={"allow_objects": True})
        OmegaConf.set_readonly(config_copy, False)
        OmegaConf.set_struct(config_copy, False)
        config_copy._set_parent(config._get_parent())
        config = config_copy

    # Finalize config (convert targets to strings, merge with kwargs)
    # TODO: kwargs are used as a config now. If it contains dataclass
    # objects, they will be interpreted as config nodes in the
    # instantiation result. We might want to change that behavior.
    _convert_container_targets_to_strings(config)
    _convert_container_targets_to_strings(kwargs)
    if kwargs:
        _merge_overrides_into_config(config, kwargs)

    # Override parent modes from config if specified
    # Cannot use pop with default because of OmegaConf typed config
    # Also interpret python None as Mode.NONE
    if isinstance(config, dict) or OmegaConf.is_dict(config):
        parse = config.pop(_Keys.PARSE) if _Keys.PARSE in config else parse
        parse = ParseMode(parse if parse is not None else ParseMode.NONE)
        convert = config.pop(_Keys.CONVERT) if _Keys.CONVERT in config else convert
        convert = ConvertMode(convert if convert is not None else ConvertMode.NONE)
        recursive = (
            config.pop(_Keys.RECURSIVE) if _Keys.RECURSIVE in config else recursive
        )
        if not isinstance(recursive, bool):
            raise TypeError(f"_recursive_ flag must be a bool, got {type(recursive)}")

    # Parse as OmegaConf container if dict, list or structured config
    if parse == ParseMode.OMEGACONF and (isinstance(config, (dict, list))):
        config = OmegaConf.structured(config, flags={"allow_objects": True})

    # Parse as native dict if OmegaConf container
    if parse == ParseMode.NATIVE and OmegaConf.is_config(config):
        config = OmegaConf.to_container(config, resolve=True)

    # If list, create new list of instances if recursive else config
    if isinstance(config, list):
        if recursive:
            result = []
            for item in config:
                result.append(
                    instantiate(item, parse=parse, convert=convert, recursive=recursive)
                )
            return result
        else:
            return config

    # If OmegaConf list, create new list of instances if recursive
    if OmegaConf.is_list(config):
        if recursive:
            # If ALL or PARTIAL, instantiate in list
            if convert in (ConvertMode.ALL, ConvertMode.PARTIAL):
                return [
                    instantiate(item, parse=parse, convert=convert, recursive=recursive)
                    for item in config._iter_ex(resolve=True)
                ]

            # Otherwise, new OmegaConf container
            lst = OmegaConf.create([], flags={"allow_objects": True})
            lst._set_parent(config)
            for item in config._iter_ex(resolve=False):
                lst.append(
                    instantiate(item, parse=parse, convert=convert, recursive=recursive)
                )
            lst._metadata.object_type = config._metadata.object_type
            return lst

        else:
            if convert == ConvertMode.ALL:
                return OmegaConf.to_container(config, resolve=True)
            if convert == ConvertMode.PARTIAL:
                return OmegaConf.to_container(
                    config, resolve=True, exclude_structured_configs=True
                )
            return config

    if isinstance(config, dict):
        target = (
            _resolve_target(config.pop(_Keys.TARGET)) if _is_target(config) else None
        )
        if recursive:
            final_kwargs = {}
            for key, value in config.items():
                final_kwargs[key] = instantiate(
                    value, parse=parse, convert=convert, recursive=recursive
                )
        else:
            final_kwargs = config
        if target:
            return _call_target(target, *args, **final_kwargs)
        else:
            if args:
                raise ValueError(
                    f"No target found in config {config} but args = {args} (should be empty)"
                )
            return final_kwargs

    if OmegaConf.is_dict(config):
        if _is_target(config):
            target = _resolve_target(config.pop(_Keys.TARGET))
            if recursive:
                final_kwargs = {}
                for key, value in config.items_ex(resolve=True):
                    final_kwargs[key] = instantiate(
                        value, parse=parse, convert=convert, recursive=recursive
                    )
            else:
                final_kwargs = config
            return _call_target(target, *args, **final_kwargs)

        if recursive:
            # If ALL or PARTIAL non structured, instantiate in dict
            if convert == ConvertMode.ALL or (
                convert == ConvertMode.PARTIAL and config._metadata.object_type is None
            ):
                final_kwargs = {}
                for key, value in config.items_ex(resolve=True):
                    final_kwargs[key] = instantiate(
                        value, parse=parse, convert=convert, recursive=recursive
                    )
                return final_kwargs

            # Otherwise, new OmegaConf container
            cfg = OmegaConf.create({}, flags={"allow_objects": True})
            for key, value in config.items_ex(resolve=False):
                cfg[key] = instantiate(
                    value, parse=parse, convert=convert, recursive=recursive
                )
            cfg._set_parent(config)
            cfg._metadata.object_type = config._metadata.object_type

            # If convert is PARTIAL, convert container
            if convert == ConvertMode.PARTIAL:
                return OmegaConf.to_container(
                    cfg, resolve=True, exclude_structured_configs=True
                )
            return cfg
        else:
            if convert == ConvertMode.ALL:
                return OmegaConf.to_container(config, resolve=True)
            if convert == ConvertMode.PARTIAL:
                return OmegaConf.to_container(
                    config, resolve=True, exclude_structured_configs=True
                )
            return config

    # Default case, return config (no target or recursive to handle)
    return config


# Alias for instantiate
call = instantiate


def get_class(path: str) -> type:
    try:
        cls = _locate(path)
        if not isinstance(cls, type):
            raise ValueError(f"Located non-class in {path} : {type(cls).__name__}")
        return cls
    except Exception as e:
        log.error(f"Error initializing class at {path} : {e}")
        raise e


def get_method(path: str) -> Callable[..., Any]:
    try:
        cl = _locate(path)
        if not callable(cl):
            raise ValueError(f"Non callable object located : {type(cl).__name__}")
        return cl
    except Exception as e:
        log.error(f"Error getting callable at {path} : {e}")
        raise e


# Alias for get_method
get_static_method = get_method


def get_original_cwd() -> str:
    """
    :return: the original working directory the Hydra application was launched from
    """
    if not HydraConfig.initialized():
        raise ValueError(
            "get_original_cwd() must only be used after HydraConfig is initialized"
        )
    ret = HydraConfig.get().runtime.cwd
    assert ret is not None and isinstance(ret, str)
    return ret


def to_absolute_path(path: str) -> str:
    """
    converts the specified path to be absolute path.
    if the input path is relative, it's interpreted as relative to the original working directory
    if it's absolute, it's returned as is
    :param path: path to convert
    :return:
    """
    p = Path(path)
    if not HydraConfig.initialized():
        base = Path(os.getcwd())
    else:
        base = Path(get_original_cwd())
    if p.is_absolute():
        ret = p
    else:
        ret = base / p
    return str(ret)
