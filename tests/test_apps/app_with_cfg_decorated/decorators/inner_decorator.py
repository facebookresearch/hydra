# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from functools import wraps

from omegaconf import DictConfig


def inner_decorator(func):  # type: ignore[no-untyped-def]
    @wraps(func)
    def wrapper(conf: DictConfig):  # type: ignore[no-untyped-def]
        assert conf.dataset.path == "/datasets/imagenet"
        return func(conf)

    return wrapper
