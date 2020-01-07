# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
from typing import Callable, Optional

from ._internal.utils import get_args_parser, run_hydra
from .types import TaskFunction

# TODO: change config_path to Optional[str]


def main(
    config_path: str = "", strict: Optional[bool] = None
) -> Callable[[TaskFunction], Callable[[], None]]:
    """
    :param config_path: the config path, can be a directory in which it's used as the config root
    or a file to load
    :param strict: strict mode, will throw an error if command line overrides are not changing an
    existing key or
           if the code is accessing a non existent key
    """

    def main_decorator(task_function: TaskFunction) -> Callable[[], None]:
        @functools.wraps(task_function)
        def decorated_main() -> None:
            run_hydra(
                args_parser=get_args_parser(),
                task_function=task_function,
                config_path=config_path,
                strict=strict,
            )

        return decorated_main

    return main_decorator
