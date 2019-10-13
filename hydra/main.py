# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
import sys
from ._internal.utils import run_hydra, get_args_parser


def main(config_path="", strict=None):
    """
    :param config_path: the config path, can be a directory in which it's used as the config root
    or a file to load
    :param strict: strict mode, will throw an error if command line overrides are not changing an
    existing key or
           if the code is accessing a non existent key
    """

    def main_decorator(task_function):
        @functools.wraps(task_function)
        def decorated_main():
            try:
                run_hydra(
                    args_parser=get_args_parser(),
                    task_function=task_function,
                    config_path=config_path,
                    strict=strict,
                )
            except KeyboardInterrupt:
                sys.exit(-1)
            except SystemExit:
                pass

        return decorated_main

    return main_decorator
