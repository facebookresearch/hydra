# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging.config
import collections
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from omegaconf import OmegaConf

from hydra._internal.utils import (
    _convert_target_to_string,
    _get_target_type,
    _locate,
    _pop_convert_mode,
    _is_recursive,
)
from hydra.core.hydra_config import HydraConfig

log = logging.getLogger(__name__)


class ConvertMode(str, Enum):
    # Use DictConfig/ListConfig
    NONE = "none"
    # Convert the OmegaConf config to primitive container, Structured Configs are preserved
    PARTIAL = "partial"
    # Fully convert the OmegaConf config to primitive containers (dict, list and primitives).
    ALL = "all"


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
    :return: if _target_ is a class name: the instantiated object
             if _target_ is a callable: the return value of the call
    """

    def _rec_instantiate(cfg):
        recursive = _is_recursive(config, {})
        if not recursive:
            return cfg
        if isinstance(cfg, collections.MutableSequence):
            return [_rec_instantiate(it) for it in cfg]
        if isinstance(cfg, collections.MutableMapping):
            if "_target_" in cfg:
                target = _get_target_type(cfg, {})
                # Do not repack kwargs in OmegaConf object
                return target(**{key: _rec_instantiate(value) for key, value in cfg.items()})
            else:
                # Keep original type (OmegaConfg DictConfig or dict)
                for key, value in cfg.items():
                    cfg[key] = _rec_instantiate(value)
                return cfg
        return cfg

    try:
        convert_mode = ConvertMode(kwargs.get("_convert_", "none"))
        if convert_mode is ConvertMode.ALL:
            # Resolve config then instantiate
            config = OmegaConf.to_container(config, resolve=True)
            return _rec_instantiate(config)
        if convert_mode is ConvertMode.PARTIAL:
            # Instantiate, keep OmegaConf objects
            return _rec_instantiate(config)
        if convert_mode is ConvertMode.NONE:
            # Do nothing
            return config
        raise ValueError(f"convert_mode {convert_mode} unknown.")
    except Exception as e:
        # preserve the original exception backtrace
        raise type(e)(
            f"Error instantiating/calling '{_convert_target_to_string(config)}' : {e}"
        ).with_traceback(sys.exc_info()[2])


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
