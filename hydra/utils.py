# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging.config
import os
from pathlib import Path
from typing import Any, Callable

import hydra._internal.instantiate._instantiate2
import hydra.types
from hydra._internal.utils import _locate
from hydra.core.hydra_config import HydraConfig

log = logging.getLogger(__name__)

# Instantiation related symbols
instantiate = hydra._internal.instantiate._instantiate2.instantiate
call = instantiate
ConvertMode = hydra.types.ConvertMode


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
