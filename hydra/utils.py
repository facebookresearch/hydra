# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging.config
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from omegaconf import OmegaConf
from omegaconf._utils import is_structured_config

from hydra._internal.utils import (
    _convert_container_targets_to_strings,
    _convert_target_to_string,
    _get_kwargs,
    _get_target_type,
    _locate,
    _pop_convert_mode,
)
from hydra.core.hydra_config import HydraConfig
from hydra.errors import HydraException, InstantiationException
from hydra.types import TargetConf

log = logging.getLogger(__name__)


class ConvertMode(Enum):
    # Use DictConfig/ListConfig
    NONE = 0
    # Convert the OmegaConf config to primitive container, Structured Configs are preserved
    PARTIAL = 1
    # Fully convert the OmegaConf config to primitive containers (dict, list and primitives).
    ALL = 2


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

    if OmegaConf.is_none(config):
        return None

    if isinstance(config, TargetConf) and config._target_ == "???":
        # Specific check to give a good warning about failure to annotate _target_ as a string.
        raise InstantiationException(
            f"Missing value for {type(config).__name__}._target_. Check that it's properly annotated and overridden."
            f"\nA common problem is forgetting to annotate _target_ as a string : '_target_: str = ...'"
        )

    if not (
        isinstance(config, dict)
        or OmegaConf.is_config(config)
        or is_structured_config(config)
    ):
        raise HydraException(f"Unsupported config type : {type(config).__name__}")

    if isinstance(config, dict):
        configc = config.copy()
        _convert_container_targets_to_strings(configc)
        config = configc

    kwargsc = kwargs.copy()
    _convert_container_targets_to_strings(kwargsc)
    kwargs = kwargsc

    # make a copy to ensure we do not change the provided object
    config_copy = OmegaConf.structured(config, flags={"allow_objects": True})
    if OmegaConf.is_config(config):
        config_copy._set_parent(config._get_parent())
    config = config_copy
    assert OmegaConf.is_config(config)
    OmegaConf.set_readonly(config, False)
    OmegaConf.set_struct(config, False)

    target = _get_target_type(config, kwargs)
    try:
        config._set_flag("allow_objects", True)
        final_kwargs = _get_kwargs(config, **kwargs)
        convert = _pop_convert_mode(final_kwargs)
        if convert == ConvertMode.PARTIAL:
            final_kwargs = OmegaConf.to_container(
                final_kwargs, resolve=True, exclude_structured_configs=True
            )
            return target(*args, **final_kwargs)
        elif convert == ConvertMode.ALL:
            final_kwargs = OmegaConf.to_container(final_kwargs, resolve=True)
            return target(*args, **final_kwargs)
        elif convert == ConvertMode.NONE:
            return target(*args, **final_kwargs)
        else:
            assert False
    except Exception as e:
        # preserve the original exception backtrace
        raise type(e)(
            f"Error instantiating/calling '{_convert_target_to_string(target)}' : {e}"
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
