# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from functools import wraps
from typing import Callable, TypeVar

from omegaconf import DictConfig

R = TypeVar("R")


def inner_decorator(func: Callable[[DictConfig], R]) -> Callable[[DictConfig], R]:
    @wraps(func)
    def wrapper(conf: DictConfig) -> R:
        assert conf.dataset.path == "/datasets/imagenet"
        return func(conf)

    return wrapper
