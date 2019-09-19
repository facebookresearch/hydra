# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
import sys
import hydra
from ._internal.utils import run_hydra, get_args


def main(config_path="", strict=False):
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
                    get_args(version=hydra.__version__),
                    task_function,
                    config_path,
                    strict,
                )
            except KeyboardInterrupt:
                sys.exit(-1)
            except SystemExit:
                pass

        return decorated_main

    return main_decorator
