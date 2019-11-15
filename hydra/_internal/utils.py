# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import inspect
import os
import sys

from .hydra import Hydra
from ..plugins.common.utils import split_config_path


def run_hydra(args_parser, task_function, config_path, strict):
    stack = inspect.stack()
    frame = stack[2]

    calling_file = None
    calling_module = None
    try:
        calling_file = frame[0].f_locals["__file__"]
    except KeyError:
        pass
    try:
        module_envs = ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE", "FB_XAR_MAIN_MODULE"]
        for module_env in module_envs:
            if module_env in os.environ:
                calling_module = os.environ[module_env]
                break

        if calling_module is None:
            calling_module = frame[0].f_globals[frame[3]].__module__
    except KeyError:
        pass

    config_dir, config_file = split_config_path(config_path)
    strict = _strict_mode_strategy(strict, config_file)

    hydra = Hydra.create_main_hydra_file_or_module(
        calling_file=calling_file,
        calling_module=calling_module,
        config_dir=config_dir,
        strict=strict,
    )

    args = args_parser.parse_args()
    if args.help:
        hydra.app_help(config_file=config_file, args_parser=args_parser, args=args)
        sys.exit(0)
    if args.hydra_help:
        hydra.hydra_help(config_file=config_file, args_parser=args_parser, args=args)
        sys.exit(0)

    has_show_cfg = args.cfg is not None
    num_commands = args.run + has_show_cfg + args.multirun + args.shell_completion
    if num_commands > 1:
        raise ValueError(
            "Only one of --run, --multirun,  -cfg and --shell_completion can be specified"
        )
    if num_commands == 0:
        args.run = True
    if args.run:
        hydra.run(
            config_file=config_file,
            task_function=task_function,
            overrides=args.overrides,
        )
    elif args.multirun:
        hydra.multirun(
            config_file=config_file,
            task_function=task_function,
            overrides=args.overrides,
        )
    elif args.cfg:
        hydra.show_cfg(overrides=args.overrides, cfg_type=args.cfg)
    elif args.shell_completion:
        hydra.shell_completion(config_file=config_file, overrides=args.overrides)
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


def get_args_parser():
    from .. import __version__

    parser = argparse.ArgumentParser(add_help=False, description="Hydra")
    parser.add_argument("--help", "-h", action="store_true", help="Application's help")
    parser.add_argument("--hydra-help", action="store_true", help="Hydra's help")
    parser.add_argument(
        "--version", action="version", version="Hydra {}".format(__version__)
    )
    parser.add_argument(
        "overrides",
        nargs="*",
        help="Any key=value arguments to override config values (use dots for.nested=overrides)",
    )

    parser.add_argument(
        "--cfg",
        "-c",
        choices=["job", "hydra", "all"],
        help="Show config instead of running [job|hydra|all]",
    )

    parser.add_argument("--run", "-r", action="store_true", help="Run a job")

    parser.add_argument(
        "--multirun",
        "-m",
        action="store_true",
        help="Run multiple jobs with the configured launcher",
    )

    shell = "SHELL_NAME"
    install_cmd = 'eval "$({} -sc install={})"'.format(_get_exec_command(), shell)
    uninstall_cmd = 'eval "$({} -sc uninstall={})"'.format(_get_exec_command(), shell)
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
    return parser


def get_args(args=None):
    return get_args_parser().parse_args(args=args)


def _strict_mode_strategy(strict, config_file):
    """Decide how to set strict mode.
    If a value was provided -- always use it. Otherwise decide based
    on the existence of config_file.
    """

    if strict is not None:
        return strict

    # strict if config_file is present
    return config_file is not None
