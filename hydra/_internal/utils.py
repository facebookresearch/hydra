# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import copy
import inspect
import logging.config
import os
import sys
import warnings
from os.path import dirname, join, normpath, realpath
from traceback import print_exc
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, Union

from omegaconf import DictConfig, OmegaConf, _utils, read_write
from omegaconf.errors import OmegaConfBaseException

from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.utils import get_valid_filename, split_config_path
from hydra.errors import HydraException
from hydra.types import ObjectConf, TaskFunction

log = logging.getLogger(__name__)


def _get_module_name_override() -> Optional[str]:
    module_envs = ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE", "FB_XAR_MAIN_MODULE"]
    for module_env in module_envs:
        if module_env in os.environ:
            return os.environ[module_env]
    return None


def detect_calling_file_or_module_from_task_function(
    task_function: Any,
) -> Tuple[Optional[str], Optional[str], str]:
    mdl = _get_module_name_override()
    calling_file: Optional[str]
    calling_module: Optional[str]
    if mdl is not None:
        calling_file = None
        # short module name
        if mdl.rfind(".") == -1:
            calling_module = "__main__"
        else:
            calling_module = mdl
    else:
        calling_file = task_function.__code__.co_filename
        calling_module = None

    task_name = detect_task_name(calling_file, mdl)

    return calling_file, calling_module, task_name


def detect_calling_file_or_module_from_stack_frame(
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
        calling_module = _get_module_name_override()
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
    config_path: Optional[str],
) -> str:
    if calling_module is not None:
        last_dot = calling_module.rfind(".")
        if last_dot != -1:
            calling_module = calling_module[0:last_dot]

        if config_path is not None:
            config_path = config_path.replace(os.path.sep, "/")
            while str.startswith(config_path, "../"):
                config_path = config_path[len("../") :]
                last_dot = calling_module.rfind(".")
                if last_dot != -1:
                    calling_module = calling_module[0:last_dot]
                else:
                    calling_module = ""

        search_path_dir = "pkg://" + calling_module

        if config_path is not None:
            if calling_module != "":
                search_path_dir = search_path_dir + "/" + config_path
            else:
                search_path_dir = search_path_dir + config_path
    elif calling_file is not None:
        abs_base_dir = realpath(dirname(calling_file))

        if config_path is not None:
            search_path_dir = join(abs_base_dir, config_path)
        else:
            search_path_dir = abs_base_dir
        search_path_dir = normpath(search_path_dir)
    else:
        raise ValueError()

    return search_path_dir


def create_automatic_config_search_path(
    calling_file: Optional[str],
    calling_module: Optional[str],
    config_path: Optional[str],
) -> ConfigSearchPath:
    search_path_dir = compute_search_path_dir(calling_file, calling_module, config_path)
    return create_config_search_path(search_path_dir)


def create_config_search_path(search_path_dir: Optional[str]) -> ConfigSearchPath:
    from hydra.core.plugins import Plugins
    from hydra.plugins.search_path_plugin import SearchPathPlugin

    search_path = ConfigSearchPathImpl()
    search_path.append("hydra", "pkg://hydra.conf")

    if search_path_dir is not None:
        search_path.append("main", search_path_dir)

    search_path_plugins = Plugins.instance().discover(SearchPathPlugin)
    for spp in search_path_plugins:
        plugin = spp()
        assert isinstance(plugin, SearchPathPlugin)
        plugin.manipulate_search_path(search_path)

    search_path.append("schema", "structured://")

    return search_path


def run_and_report(func: Any) -> Any:
    try:
        return func()
    except (HydraException, OmegaConfBaseException) as ex:
        if "HYDRA_FULL_ERROR" in os.environ and os.environ["HYDRA_FULL_ERROR"] == "1":
            print_exc()
        else:
            sys.stderr.write(str(ex) + "\n")
            if ex.__cause__ is not None:
                sys.stderr.write(str(ex.__cause__) + "\n")

            sys.stderr.write(
                "\nSet the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\n"
            )
        sys.exit(1)


def run_hydra(
    args_parser: argparse.ArgumentParser,
    task_function: TaskFunction,
    config_path: Optional[str],
    config_name: Optional[str],
    strict: Optional[bool],
) -> None:

    from hydra.core.global_hydra import GlobalHydra

    from .hydra import Hydra

    args = args_parser.parse_args()
    if args.config_name is not None:
        config_name = args.config_name

    if args.config_path is not None:
        config_path = args.config_path

    (
        calling_file,
        calling_module,
        task_name,
    ) = detect_calling_file_or_module_from_task_function(task_function)

    config_dir, config_name = split_config_path(config_path, config_name)

    search_path = create_automatic_config_search_path(
        calling_file, calling_module, config_dir
    )

    hydra = run_and_report(
        lambda: Hydra.create_main_hydra2(
            task_name=task_name, config_search_path=search_path, strict=strict
        )
    )

    try:
        if args.help:
            hydra.app_help(config_name=config_name, args_parser=args_parser, args=args)
            sys.exit(0)
        if args.hydra_help:
            hydra.hydra_help(
                config_name=config_name, args_parser=args_parser, args=args
            )
            sys.exit(0)

        has_show_cfg = args.cfg is not None
        num_commands = (
            args.run + has_show_cfg + args.multirun + args.shell_completion + args.info
        )
        if num_commands > 1:
            raise ValueError(
                "Only one of --run, --multirun,  -cfg, --info and --shell_completion can be specified"
            )
        if num_commands == 0:
            args.run = True
        if args.run:
            run_and_report(
                lambda: hydra.run(
                    config_name=config_name,
                    task_function=task_function,
                    overrides=args.overrides,
                )
            )
        elif args.multirun:
            run_and_report(
                lambda: hydra.multirun(
                    config_name=config_name,
                    task_function=task_function,
                    overrides=args.overrides,
                )
            )
        elif args.cfg:
            run_and_report(
                lambda: hydra.show_cfg(
                    config_name=config_name,
                    overrides=args.overrides,
                    cfg_type=args.cfg,
                    package=args.package,
                )
            )
        elif args.shell_completion:
            run_and_report(
                lambda: hydra.shell_completion(
                    config_name=config_name, overrides=args.overrides
                )
            )
        elif args.info:
            hydra.show_info(config_name=config_name, overrides=args.overrides)
        else:
            sys.stderr.write("Command not specified\n")
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


def _get_completion_help() -> str:
    from hydra.core.plugins import Plugins
    from hydra.plugins.completion_plugin import CompletionPlugin

    completion_plugins = Plugins.instance().discover(CompletionPlugin)
    completion_info: List[str] = []
    for plugin_cls in completion_plugins:
        assert issubclass(plugin_cls, CompletionPlugin)
        for cmd in ["install", "uninstall"]:
            head = f"{plugin_cls.provides().capitalize()} - {cmd.capitalize()}:"
            completion_info.append(head)
            completion_info.append(plugin_cls.help(cmd).format(_get_exec_command()))
        completion_info.append("")
    completion_help = "\n".join([f"    {x}" if x else x for x in completion_info])
    return completion_help


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

    parser.add_argument(
        "--package", "-p", help="Config package to show",
    )

    parser.add_argument("--run", "-r", action="store_true", help="Run a job")

    parser.add_argument(
        "--multirun",
        "-m",
        action="store_true",
        help="Run multiple jobs with the configured launcher",
    )

    parser.add_argument(
        "--shell-completion",
        "-sc",
        action="store_true",
        help=f"Install or Uninstall shell completion:\n{_get_completion_help()}",
    )

    parser.add_argument(
        "--config-path",
        "-cp",
        help="""Overrides the config_path specified in hydra.main().
                    The config_path is relative to the Python file declaring @hydra.main()""",
    )

    parser.add_argument(
        "--config-name",
        "-cn",
        help="Overrides the config_name specified in hydra.main()",
    )

    parser.add_argument(
        "--info", "-i", action="store_true", help="Print Hydra information",
    )
    return parser


def get_args(args: Optional[Sequence[str]] = None) -> Any:
    return get_args_parser().parse_args(args=args)


def get_column_widths(matrix: List[List[str]]) -> List[int]:
    num_cols = 0
    for row in matrix:
        num_cols = max(num_cols, len(row))
    widths: List[int] = [0] * num_cols
    for row in matrix:
        for idx, col in enumerate(row):
            widths[idx] = max(widths[idx], len(col))

    return widths


def _instantiate_class(
    clazz: Type[Any], config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any
) -> Any:
    final_kwargs = _get_kwargs(config, **kwargs)
    return clazz(*args, **final_kwargs)


def _call_callable(
    fn: Callable[..., Any],
    config: Union[ObjectConf, DictConfig],
    *args: Any,
    **kwargs: Any,
) -> Any:
    final_kwargs = _get_kwargs(config, **kwargs)
    return fn(*args, **final_kwargs)


def _locate(path: str) -> Union[type, Callable[..., Any]]:
    """
    Locate an object by name or dotted path, importing as necessary.
    This is similar to the pydoc function `locate`, except that it checks for
    the module from the given path from back to front.
    """
    import builtins
    from importlib import import_module

    parts = [part for part in path.split(".") if part]
    module = None
    for n in reversed(range(len(parts))):
        try:
            module = import_module(".".join(parts[:n]))
        except Exception as e:
            if n == 0:
                log.error(f"Error loading module {path} : {e}")
                raise e
            continue
        if module:
            break
    if module:
        obj = module
    else:
        obj = builtins
    for part in parts[n:]:
        if not hasattr(obj, part):
            raise ValueError(
                f"Error finding attribute ({part}) in class ({obj.__name__}): {path}"
            )
        obj = getattr(obj, part)
    if isinstance(obj, type):
        obj_type: type = obj
        return obj_type
    elif callable(obj):
        obj_callable: Callable[..., Any] = obj
        return obj_callable
    else:
        # dummy case
        raise ValueError(f"Invalid type ({type(obj)}) found for {path}")


def _get_kwargs(config: Union[ObjectConf, DictConfig], **kwargs: Any) -> Any:
    # copy config to avoid mutating it when merging with kwargs
    config_copy = copy.deepcopy(config)

    # Manually set parent as deepcopy does not currently handles it (https://github.com/omry/omegaconf/issues/130)
    # noinspection PyProtectedMember
    config_copy._set_parent(config._get_parent())  # type: ignore
    config = config_copy

    params = config.params if "params" in config else OmegaConf.create()
    assert isinstance(
        params, DictConfig
    ), f"Input config params are expected to be a mapping, found {type(config.params).__name__}"
    primitives = {}
    rest = {}
    for k, v in kwargs.items():
        if _utils.is_primitive_type(v) or isinstance(v, (dict, list)):
            primitives[k] = v
        else:
            rest[k] = v
    final_kwargs = {}
    with read_write(params):
        params.merge_with(OmegaConf.create(primitives))

    for k, v in params.items():
        final_kwargs[k] = v

    for k, v in rest.items():
        final_kwargs[k] = v
    return final_kwargs


def _get_cls_name(config: Union[ObjectConf, DictConfig]) -> str:
    if "class" in config:
        warnings.warn(
            "\n"
            "ObjectConf field 'class' is deprecated since Hydra 1.0.0 and will be removed in a future Hydra version.\n"
            "Offending config class:\n"
            f"\tclass={config['class']}\n"
            "Change your config to use 'cls' instead of 'class'.\n",
            category=UserWarning,
        )
        classname = config["class"]
        assert isinstance(classname, str)
        return classname
    else:
        if "cls" in config:
            return config.cls
        else:
            raise ValueError("Input config does not have a cls field")
