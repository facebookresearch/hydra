# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
import os
import sys
from .hydra import Hydra
import argparse


def run_hydra(args_parser, task_function, config_path, strict):
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
        strict=strict,
    )

    args = args_parser.parse_args()
    if args.help:
        hydra.app_help(args_parser=args_parser, args=args)
        sys.exit(0)
    if args.hydra_help:
        hydra.hydra_help(args_parser=args_parser, args=args)
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
        hydra.run(overrides=args.overrides)
    elif args.multirun:
        hydra.multirun(overrides=args.overrides)
    elif args.cfg:
        hydra.show_cfg(overrides=args.overrides, cfg_type=args.cfg)
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
