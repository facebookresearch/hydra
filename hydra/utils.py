# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging.config
from pathlib import Path
from typing import Any, Callable, Union

from omegaconf import DictConfig

from hydra._internal._utils_impl import (
    _call_callable,
    _get_cls_name,
    _instantiate_class,
    _locate,
)
from hydra.core.hydra_config import HydraConfig
from hydra.types import ObjectConf

log = logging.getLogger(__name__)


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


def call(config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any) -> Any:
    cls = _get_cls_name(config)
    try:
        type_or_callable = _locate(cls)
        if isinstance(type_or_callable, type):
            return _instantiate_class(type_or_callable, config, *args, **kwargs)
        else:
            assert callable(type_or_callable)
            return _call_callable(type_or_callable, config, *args, **kwargs)
    except Exception as e:
        log.error(f"Error instantiating '{cls}' : {e}")
        raise e


# Alias for call
instantiate = call


def get_original_cwd() -> str:
    ret = HydraConfig.instance().hydra.runtime.cwd
    assert ret is not None and isinstance(ret, str)
    return ret


def to_absolute_path(path: str) -> str:
    """
    converts the specified path to be absolute path.
    if the input path is relative, it's interpreted as relative to the original working directory
    if it's absolute, it's returned as is
    :param path:
    :return:
    """
    p = Path(path)
    if p.is_absolute():
        ret = p
    else:
        ret = Path(get_original_cwd()) / p
    return str(ret)
