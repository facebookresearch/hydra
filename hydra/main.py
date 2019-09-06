# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import functools
import sys

import hydra
from ._internal.utils import run_hydra


def get_args():
    parser = argparse.ArgumentParser(description="Hydra")
    version = hydra.__version__
    parser.add_argument(
        "--version", action="version", version="Hydra {}".format(version)
    )
    parser.add_argument(
        "overrides",
        nargs="*",
        help="Any key=value arguments to override config values (use dots for.nested=overrides)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="Activate debug logging, otherwise takes a comma separated list of loggers ('root' for root logger)",
        nargs="?",
        default=None,
    )

    parser.add_argument("--cfg", "-c", action="store_true", help="Show config")

    parser.add_argument("--run", "-r", action="store_true", help="Run a job")

    parser.add_argument(
        "--multirun",
        "-m",
        action="store_true",
        help="Run multiple jobs with the configured launcher",
    )

    parser.add_argument(
        "--shell_completion",
        "-sc",
        action="store_true",
        help="Install/Uninstall shell completion",
    )

    return parser.parse_args()


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
                run_hydra(get_args(), task_function, config_path, strict)
            except KeyboardInterrupt:
                sys.exit(-1)
            except SystemExit:
                pass

        return decorated_main

    return main_decorator
