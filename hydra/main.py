# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
from typing import Any, Callable, Optional

from omegaconf import DictConfig

from ._internal.utils import _run_hydra, get_args_parser
from .types import TaskFunction


def main(
    config_path: Optional[str] = None,
    config_name: Optional[str] = None,
    strict: Optional[bool] = None,
) -> Callable[[TaskFunction], Any]:
    """
    :param config_path: the config path, a directory relative to the declaring python file.
    :param config_name: the name of the config (usually the file name without the .yaml extension)
    :param strict: (Deprecated) strict mode, will throw an error if command line overrides are not changing an
    existing key or if the code is accessing a non existent key
    """

    def main_decorator(task_function: TaskFunction) -> Callable[[], None]:
        @functools.wraps(task_function)
        def decorated_main(cfg_passthrough: Optional[DictConfig] = None) -> Any:
            if cfg_passthrough is not None:
                return task_function(cfg_passthrough)
            else:
                args = get_args_parser()
                # no return value from run_hydra() as it may sometime actually run the task_function
                # multiple times (--multirun)
                _run_hydra(
                    args_parser=args,
                    task_function=task_function,
                    config_path=config_path,
                    config_name=config_name,
                    strict=strict,
                )

        return decorated_main

    return main_decorator
