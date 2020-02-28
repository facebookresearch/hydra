# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import inspect
import os
import sys
from os.path import dirname, join, normpath, realpath
from typing import Any, List, Optional, Sequence, Tuple

from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.utils import get_valid_filename, split_config_path
from hydra.types import TaskFunction


def detect_calling_file_or_module(
    stack_depth: int,
) -> Tuple[Optional[str], Optional[str]]:
    calling_file = None
    calling_module = None

    stack = inspect.stack()
    frame = stack[stack_depth]
    if is_notebook():
        pynb_dir = frame[0].f_globals["_dh"][0]
        calling_file = join(pynb_dir, "notebook.ipynb")
        return calling_file, None

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
        try:
            calling_module = frame[0].f_locals["self"].__module__
        except KeyError:
            pass

    return calling_file, calling_module


def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__  # type: ignore
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


def detect_task_name(calling_file: Optional[str], calling_module: Optional[str]) -> str:

    if calling_file is not None:
        target_file = os.path.basename(calling_file)
        task_name = get_valid_filename(os.path.splitext(target_file)[0])
    elif calling_module is not None:
        last_dot = calling_module.rfind(".")
        if last_dot != -1:
            task_name = calling_module[last_dot + 1 :]
        else:
            task_name = calling_module
    else:
        raise ValueError()

    return task_name


def compute_search_path_dir(
    calling_file: Optional[str],
    calling_module: Optional[str],
    config_dir: Optional[str],
) -> str:
    if calling_module is not None:
        last_dot = calling_module.rfind(".")
        if last_dot != -1:
            calling_module = calling_module[0:last_dot]

        if config_dir is not None:
            config_dir = config_dir.replace(os.path.sep, "/")
            while str.startswith(config_dir, "../"):
                config_dir = config_dir[len("../") :]
                last_dot = calling_module.rfind(".")
                if last_dot != -1:
                    calling_module = calling_module[0:last_dot]
                else:
                    calling_module = ""

        search_path_dir = "pkg://" + calling_module

        if config_dir is not None:
            if calling_module != "":
                search_path_dir = search_path_dir + "/" + config_dir
            else:
                search_path_dir = search_path_dir + config_dir
    elif calling_file is not None:
        abs_base_dir = realpath(dirname(calling_file))

        if config_dir is not None:
            search_path_dir = join(abs_base_dir, config_dir)
        else:
            search_path_dir = abs_base_dir
        search_path_dir = normpath(search_path_dir)
    else:
        raise ValueError()

    return search_path_dir


def create_automatic_config_search_path(
    calling_file: Optional[str],
    calling_module: Optional[str],
    config_dir: Optional[str],
) -> ConfigSearchPath:
    search_path_dir = compute_search_path_dir(calling_file, calling_module, config_dir)
    return create_config_search_path(search_path_dir)


def create_config_search_path(search_path_dir: Optional[str]) -> ConfigSearchPath:
    from hydra.core.plugins import Plugins
    from hydra.plugins.search_path_plugin import SearchPathPlugin

    Plugins.register_config_sources()
    search_path = ConfigSearchPathImpl()
    search_path.append("hydra", "pkg://hydra.conf")

    if search_path_dir is not None:
        search_path.append("main", search_path_dir)

    search_path_plugins = Plugins.discover(SearchPathPlugin)
    for spp in search_path_plugins:
        plugin = spp()
        assert isinstance(plugin, SearchPathPlugin)
        plugin.manipulate_search_path(search_path)

    search_path.append("schema", "structured://")

    return search_path


def run_hydra(
    args_parser: argparse.ArgumentParser,
    task_function: TaskFunction,
    config_path: Optional[str],
    config_name: Optional[str],
    strict: Optional[bool],
) -> None:
    from hydra.core.global_hydra import GlobalHydra

    from .hydra import Hydra

    calling_file, calling_module = detect_calling_file_or_module(3)
    config_dir, config_name = split_config_path(config_path, config_name)
    strict = _strict_mode_strategy(strict, config_name)
    task_name = detect_task_name(calling_file, calling_module)
    search_path = create_automatic_config_search_path(
        calling_file, calling_module, config_dir
    )

    hydra = Hydra.create_main_hydra2(
        task_name=task_name, config_search_path=search_path, strict=strict
    )
    try:
        args = args_parser.parse_args()
        if args.help:
            hydra.app_help(config_name=config_name, args_parser=args_parser, args=args)
            sys.exit(0)
        if args.hydra_help:
            hydra.hydra_help(
                config_name=config_name, args_parser=args_parser, args=args
            )
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
                config_name=config_name,
                task_function=task_function,
                overrides=args.overrides,
            )
        elif args.multirun:
            hydra.multirun(
                config_name=config_name,
                task_function=task_function,
                overrides=args.overrides,
            )
        elif args.cfg:
            hydra.show_cfg(
                config_name=config_name, overrides=args.overrides, cfg_type=args.cfg
            )
        elif args.shell_completion:
            hydra.shell_completion(config_name=config_name, overrides=args.overrides)
        else:
            print("Command not specified")
            sys.exit(1)
    finally:
        GlobalHydra.instance().clear()


def _get_exec_command() -> str:
    if sys.argv[0].endswith(".py"):
        return "python {}".format(sys.argv[0])
    else:
        # Running as an installed app (setuptools entry point)
        executable = os.path.basename(sys.argv[0])
        return executable


def get_args_parser() -> argparse.ArgumentParser:
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


def get_args(args: Optional[Sequence[str]] = None) -> Any:
    return get_args_parser().parse_args(args=args)


def _strict_mode_strategy(strict: Optional[bool], config_name: Optional[str]) -> bool:
    """Decide how to set strict mode.
    If a value was provided -- always use it. Otherwise decide based
    on the existence of config_name.
    """

    if strict is not None:
        return strict

    # strict if config_name is present
    return config_name is not None


def get_column_widths(matrix: List[List[str]]) -> List[int]:
    num_cols = 0
    for row in matrix:
        num_cols = max(num_cols, len(row))
    widths: List[int] = [0] * num_cols
    for row in matrix:
        for idx, col in enumerate(row):
            widths[idx] = max(widths[idx], len(col))

    return widths
