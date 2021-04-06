# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
from textwrap import dedent
from typing import Any, Callable, Optional
from warnings import warn

from omegaconf import DictConfig

from ._internal.utils import _run_hydra, get_args_parser
from .types import TaskFunction

_UNSPECIFIED_: Any = object()


def main(
    config_path: Optional[str] = _UNSPECIFIED_,
    config_name: Optional[str] = None,
) -> Callable[[TaskFunction], Any]:
    """
    :param config_path: The config path, a directory relative to the declaring python file.
                        If config_path is None no directory is added to the Config search path.
    :param config_name: The name of the config (usually the file name without the .yaml extension)
    """

    # DEPRECATED: remove in 1.2
    # in 1.2, the default config_path should be changed to None
    if config_path is _UNSPECIFIED_:
        url = "https://hydra.cc/docs/next/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"
        warn(
            category=UserWarning,
            message=dedent(
                f"""
            config_path is not specified in @hydra.main().
            See {url} for more information."""
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
