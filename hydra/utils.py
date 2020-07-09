# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging.config
import os
import warnings
from pathlib import Path
from typing import Any, Callable, Union

from omegaconf import DictConfig

from hydra._internal.utils import (
    _call_callable,
    _get_callable_name,
    _get_cls_name,
    _instantiate_class,
    _locate,
)
from hydra.core.hydra_config import HydraConfig
from hydra.errors import HydraException
from hydra.types import ObjectConf

log = logging.getLogger(__name__)


def call(config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An ObjectConf or DictConfig describing what method to call and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified method
    """
    try:
        callable_name = _get_callable_name(config)
        type_or_callable = _locate(callable_name)
        if isinstance(type_or_callable, type):
            warnings.warn(
                """Use of `hydra.utils.call` for instantiating classes is deprecated since Hydra 1.0 and support will be removed in
                Hydra 1.1. For instantiating classes, use `hydra.utils.instantiate`""",
                category=UserWarning,
            )
            return _instantiate_class(type_or_callable, config, *args, **kwargs)
        else:
            assert callable(type_or_callable)
            return _call_callable(type_or_callable, config, *args, **kwargs)
    except ValueError as e:
        raise HydraException(f"Error calling function : {e}") from e
    except Exception as e:
        raise HydraException(f"Error calling '{callable_name}' : {e}") from e


def instantiate(
    config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any
) -> Any:
    """
    :param config: An ObjectConf or DictConfig describing what class to instantiate and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified class
    """
    try:
        cls = _get_cls_name(config)
        type_or_callable = _locate(cls)
        if isinstance(type_or_callable, type):
            return _instantiate_class(type_or_callable, config, *args, **kwargs)
        else:
            warnings.warn(
                """Use of `hydra.utils.instantiate` for invoking callables is deprecated since Hydra 1.0 and support will be removed
                in Hydra 1.1. For invoking callables, use `hydra.utils.call`""",
                category=UserWarning,
            )
            assert callable(type_or_callable)
            return _call_callable(type_or_callable, config, *args, **kwargs)
    except ValueError as e:
        raise HydraException(f"Error instantiating class : {e}") from e
    except Exception as e:
        raise HydraException(f"Error instantiating '{cls}' : {e}") from e


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
