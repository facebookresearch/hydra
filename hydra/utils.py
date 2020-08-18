# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import logging.config
import os
from pathlib import Path
from typing import Any, Callable, Dict, Union

from omegaconf import DictConfig, OmegaConf

from hydra._internal.utils import (
    _call_callable,
    _get_cls_name,
    _instantiate_class,
    _locate,
)
from hydra.core.hydra_config import HydraConfig
from hydra.errors import HydraException, InstantiationException
from hydra.types import ObjectConf, TargetConf

log = logging.getLogger(__name__)


def call(
    config: Union[ObjectConf, TargetConf, DictConfig, Dict[Any, Any]],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    :param config: An object describing what to call and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified class or method
    """
    if isinstance(config, TargetConf) and config._target_ == "???":
        raise InstantiationException(
            f"Missing _target_ value. Check that you specified it in '{type(config).__name__}'"
            f" and that the type annotation is correct: '_target_: str = ...'"
        )
    if isinstance(config, (dict, ObjectConf, TargetConf)):
        config = OmegaConf.structured(config)

    if OmegaConf.is_none(config):
        return None
    cls = "<unknown>"
    try:
        assert isinstance(config, DictConfig)
        # make a copy to ensure we do not change the provided object
        config = copy.deepcopy(config)
        OmegaConf.set_readonly(config, False)
        OmegaConf.set_struct(config, False)
        cls = _get_cls_name(config)
        type_or_callable = _locate(cls)
        if isinstance(type_or_callable, type):
            return _instantiate_class(type_or_callable, config, *args, **kwargs)
        else:
            assert callable(type_or_callable)
            return _call_callable(type_or_callable, config, *args, **kwargs)
    except InstantiationException as e:
        raise e
    except Exception as e:
        raise HydraException(f"Error calling '{cls}' : {e}") from e


# Alias for call
instantiate = call


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
