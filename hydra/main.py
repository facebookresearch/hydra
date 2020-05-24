# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
from typing import Callable, Optional

from ._internal.utils import get_args_parser, run_hydra
from .types import TaskFunction


def main(
    config_path: Optional[str] = None,
    config_name: Optional[str] = None,
    strict: Optional[bool] = None,
) -> Callable[[TaskFunction], Callable[[], None]]:
    """
    :param config_path: the config path, a directory relative to the declaring python file.
    :param config_name: the name of the config (usually the file name without the .yaml extension)
    :param strict: (Deprecated) strict mode, will throw an error if command line overrides are not changing an
    existing key or if the code is accessing a non existent key
    """

    def main_decorator(task_function: TaskFunction) -> Callable[[], None]:
        @functools.wraps(task_function)
        def decorated_main() -> None:
            run_hydra(
                args_parser=get_args_parser(),
                task_function=task_function,
                config_path=config_path,
                config_name=config_name,
                strict=strict,
            )

        return decorated_main

    return main_decorator
