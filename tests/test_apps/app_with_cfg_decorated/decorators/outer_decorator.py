# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from functools import wraps

data = []


def outer_decorator(arg1: str):  # type: ignore[no-untyped-def]
    def wrapper(func):  # type: ignore[no-untyped-def]
        @wraps(func)
        def inner_wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
            data.append(arg1)
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper
