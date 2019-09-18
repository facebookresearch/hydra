# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
import os
import sys
from .hydra import Hydra
import argparse
from argparse import RawTextHelpFormatter


def run_hydra(args, task_function, config_path, strict):
    stack = inspect.stack()
    frame = stack[2]

    calling_file = None
    calling__module = None
    try:
        calling_file = frame[0].f_locals["__file__"]
    except KeyError:
        pass
    try:
        module_envs = ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE", "FB_XAR_MAIN_MODULE"]
        for module_env in module_envs:
            if module_env in os.environ:
                calling__module = os.environ[module_env]
                break

        if calling__module is None:
            calling__module = frame[0].f_globals[frame[3]].__module__
    except KeyError:
        pass

    hydra = Hydra(
        calling_file=calling_file,
        calling_module=calling__module,
        config_path=config_path,
        task_function=task_function,
        verbose=args.verbose,
        strict=strict,
    )

    num_commands = args.run + args.cfg + args.multirun + args.shell_completion
    if num_commands > 1:
        raise ValueError(
            "Only one of --run, --sweep and --cfg  --completion can be specified"
        )
    if num_commands == 0:
        args.run = True

    if args.run:
        hydra.run(overrides=args.overrides)
    elif args.multirun:
        hydra.multirun(overrides=args.overrides)
    elif args.cfg:
        hydra.show_cfg(overrides=args.overrides)
    elif args.shell_completion:
        hydra.shell_completion(overrides=args.overrides)
    else:
        print("Command not specified")
        sys.exit(1)


def _get_exec_command():
    if sys.argv[0].endswith(".py"):
        return "python {}".format(sys.argv[0])
    else:
        # Running as an installed app (setuptools entry point)
        executable = os.path.basename(sys.argv[0])
        return executable


def get_args(args=None, version=None):
    parser = argparse.ArgumentParser(
        description="Hydra", formatter_class=RawTextHelpFormatter
    )
    if version is not None:
        parser.add_argument(
            "--version", action="version", version="Hydra {}".format(version)
        )
    parser.add_argument(
        "overrides",
        nargs="*",
        help="""Any key=value arguments to override config values
(use dots for.nested=overrides)""",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="""Activate debug logging, otherwise takes a comma"
separated list of loggers ('root' for root logger)""",
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

    shell = "SHELL_NAME"
    install_cmd = 'eval "$({} -sc install={})"'.format(_get_exec_command(), shell)
    uninstall_cmd = 'eval "$({} --sc uninstall={})"'.format(_get_exec_command(), shell)
    parser.add_argument(
        "--shell_completion",
        "-sc",
        action="store_true",
        help="""Install or Uninstall shell completion:
Install:
{}

Uninstall:
{}
""".format(
            install_cmd, uninstall_cmd
        ),
    )

    return parser.parse_args(args)
