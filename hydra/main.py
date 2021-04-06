# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
from textwrap import dedent
from typing import Any, Callable, Optional
from warnings import warn

from omegaconf import DictConfig

from ._internal.utils import _run_hydra, get_args_parser
from .types import TaskFunction

_UNSPECIFIED_ = object()


def main(
    config_path: Optional[str] = _UNSPECIFIED_,
    config_name: Optional[str] = None,
) -> Callable[[TaskFunction], Any]:
    """
    :param config_path: the config path, a directory relative to the declaring python file.
    :param config_name: the name of the config (usually the file name without the .yaml extension)
    """

    if config_path is _UNSPECIFIED_:
        warn(
            category=UserWarning,
            message=dedent(
                """
            config_path is not specified in @hydra.main. Defaulting to `.`.
            To make this warning go away, specify the config_path.
            Options:
            - config_path=None   : Do not add any directory to the config searchpath.
                                   This will become the default in Hydra 1.2
                                   Recommended if you do not want to use configs defined next to your Python script.
            - config_path="conf" : Create a dedicated config directory.
                                   Recommended if you want to use configs defined next to your Python script.
                                   (Move your config files into the config directory).
            - config_path="."    : Use the directory/module of the Python script.
                                   This is the behavior in Hydra <= 1.0.
                                   Warning: Can cause surprising behavior.
                                   See https://github.com/facebookresearch/hydra/issues/1536 for more information.
            """
            ),
            stacklevel=2,
        )
        config_path = "."

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
                )

        return decorated_main

    return main_decorator
