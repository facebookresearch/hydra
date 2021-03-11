# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

# Contains Python 3.8 syntax
# flake does not like it when running on older versions of Python
# flake8: noqa
# With mypy, there does not seem to be a way to prevent an error when running in Python < 3.8.
# For this reason, I am including the code as a string (the horror).
# Once we upgrade to mypy 0.812, we should be able to use --exclude and eliminate this hack.
from typing import Any

code = """


class PosOnlyArgsClass:
    def __init__(self, a: Any, b: Any, /, **kwargs: Any) -> None:
        assert isinstance(kwargs, dict)
        self.a = a
        self.b = b
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"{self.a=},{self.b},{self.kwargs=}"

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, PosOnlyArgsClass):
            return (
                self.a == other.a and self.b == other.b and self.kwargs == other.kwargs
            )
        else:
            return NotImplemented
"""


# Dummy class to keep mypy happy
class PosOnlyArgsClass:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...


exec(code)  # nosec
