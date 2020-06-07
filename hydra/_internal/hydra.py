# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import logging
import os
import string
import warnings
from argparse import ArgumentParser
from collections import defaultdict
from typing import Any, Callable, DefaultDict, List, Optional, Sequence, Type

from omegaconf import DictConfig, OmegaConf, open_dict

from hydra._internal.utils import get_column_widths
from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.hydra_config import HydraConfig
from hydra.core.plugins import Plugins
from hydra.core.utils import (
    JobReturn,
    JobRuntime,
    configure_log,
    run_job,
    setup_globals,
)
from hydra.errors import MissingConfigException
from hydra.plugins.completion_plugin import CompletionPlugin
from hydra.plugins.config_source import ConfigSource
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction

from .config_loader_impl import ConfigLoaderImpl
from .utils import create_automatic_config_search_path, detect_task_name

log: Optional[logging.Logger] = None


class Hydra:
    @classmethod
    def create_main_hydra_file_or_module(
        cls: Type["Hydra"],
        calling_file: Optional[str],
        calling_module: Optional[str],
        config_dir: Optional[str],
        strict: Optional[bool],
    ) -> "Hydra":
        config_search_path = create_automatic_config_search_path(
            calling_file, calling_module, config_dir
        )
        task_name = detect_task_name(calling_file, calling_module)
        return Hydra.create_main_hydra2(task_name, config_search_path, strict)

    @classmethod
    def create_main_hydra2(
        cls,
        task_name: str,
        config_search_path: ConfigSearchPath,
        strict: Optional[bool],
    ) -> "Hydra":

        if strict is None:
            strict = True
        else:
            msg = (
                "\n@hydra.main(strict) flag is deprecated and will removed in the next version."
                "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/strict_mode_flag_deprecated"
            )
            warnings.warn(message=msg, category=UserWarning)

        config_loader: ConfigLoader = ConfigLoaderImpl(
            config_search_path=config_search_path, default_strict=strict
        )

        hydra = cls(task_name=task_name, config_loader=config_loader)
        from hydra.core.global_hydra import GlobalHydra

        GlobalHydra.instance().initialize(hydra)
        return hydra

    def __init__(self, task_name: str, config_loader: ConfigLoader) -> None:
        """
        :param task_name: task name
        :param config_loader: config loader
        """
        setup_globals()
        self.config_loader = config_loader

        for source in config_loader.get_sources():
            # if specified, make sure main config search path exists
            if source.provider == "main":
                if not source.exists(""):
                    raise MissingConfigException(
                        missing_cfg_file=source.path,
                        message=f"Primary config dir not found: {source}",
                    )

        JobRuntime().set("name", task_name)

    def run(
        self,
        config_name: Optional[str],
        task_function: TaskFunction,
        overrides: List[str],
    ) -> JobReturn:
        cfg = self.compose_config(
            config_name=config_name, overrides=overrides, with_log_configuration=True
        )
        HydraConfig.instance().set_config(cfg)
        return run_job(
            config=cfg,
            task_function=task_function,
            job_dir_key="hydra.run.dir",
            job_subdir_key=None,
        )

    def multirun(
        self,
        config_name: Optional[str],
        task_function: TaskFunction,
        overrides: List[str],
    ) -> Any:
        # Initial config is loaded without strict (individual job configs may have strict).
        cfg = self.compose_config(
            config_name=config_name,
            overrides=overrides,
            strict=False,
            with_log_configuration=True,
        )
        HydraConfig.instance().set_config(cfg)
        sweeper = Plugins.instance().instantiate_sweeper(
            config=cfg, config_loader=self.config_loader, task_function=task_function
        )
        task_overrides = cfg.hydra.overrides.task
        return sweeper.sweep(arguments=task_overrides)

    @staticmethod
    def get_sanitized_hydra_cfg(src_cfg: DictConfig) -> DictConfig:
        cfg = copy.deepcopy(src_cfg)
        with open_dict(cfg):
            for key in list(cfg.keys()):
                if key != "hydra":
                    del cfg[key]
        with open_dict(cfg.hydra):
            del cfg.hydra["hydra_help"]
            del cfg.hydra["help"]
        return cfg

    def show_cfg(
        self, config_name: Optional[str], overrides: List[str], cfg_type: str
    ) -> None:
        assert cfg_type in ["job", "hydra", "all"]
        cfg = self.compose_config(
            config_name=config_name, overrides=overrides, with_log_configuration=True
        )
        if cfg_type == "job":
            with open_dict(cfg):
                del cfg["hydra"]
        elif cfg_type == "hydra":
            cfg = self.get_sanitized_hydra_cfg(cfg)
        print(cfg.pretty())

    @staticmethod
    def get_shell_to_plugin_map(
        config_loader: ConfigLoader,
    ) -> DefaultDict[str, List[CompletionPlugin]]:
        shell_to_plugin: DefaultDict[str, List[CompletionPlugin]] = defaultdict(list)
        for clazz in Plugins.instance().discover(CompletionPlugin):
            assert issubclass(clazz, CompletionPlugin)
            plugin = clazz(config_loader)
            shell_to_plugin[plugin.provides()].append(plugin)

        for shell, plugins in shell_to_plugin.items():
            if len(plugins) > 1:
                lst = ",".join([type(plugin).__name__ for plugin in plugins])
                raise ValueError(f"Multiple plugins installed for {shell} : {lst}")

        return shell_to_plugin

    def shell_completion(
        self, config_name: Optional[str], overrides: List[str]
    ) -> None:
        subcommands = ["install", "uninstall", "query"]
        arguments = OmegaConf.from_dotlist(overrides)
        num_commands = sum(1 for key in subcommands if arguments[key] is not None)
        if num_commands != 1:
            raise ValueError(f"Expecting one subcommand from {subcommands} to be set")

        shell_to_plugin = self.get_shell_to_plugin_map(self.config_loader)

        def find_plugin(cmd: str) -> CompletionPlugin:
            if cmd not in shell_to_plugin:
                lst = "\n".join(["\t" + x for x in shell_to_plugin.keys()])
                raise ValueError(
                    f"No completion plugin for '{cmd}' found, available : \n{lst}"
                )
            return shell_to_plugin[cmd][0]

        if arguments.install is not None:
            plugin = find_plugin(arguments.install)
            plugin.install()
        elif arguments.uninstall is not None:
            plugin = find_plugin(arguments.uninstall)
            plugin.uninstall()
        elif arguments.query is not None:
            plugin = find_plugin(arguments.query)
            plugin.query(config_name=config_name)

    @staticmethod
    def format_args_help(args_parser: ArgumentParser) -> str:
        s = ""
        overrides: Any = None
        for action in args_parser._actions:
            if len(action.option_strings) == 0:
                overrides = action
            else:
                s += "{} : {}\n".format(",".join(action.option_strings), action.help)
        s += "Overrides : " + overrides.help
        return s

    def list_all_config_groups(self, parent: str = "") -> Sequence[str]:
        from hydra.core.object_type import ObjectType

        groups: List[str] = []
        for group in self.config_loader.list_groups(parent):
            if parent == "":
                group_name = group
            else:
                group_name = "{}/{}".format(parent, group)
            files = self.config_loader.get_group_options(group_name, ObjectType.CONFIG)
            dirs = self.config_loader.get_group_options(group_name, ObjectType.GROUP)
            if len(files) > 0:
                groups.append(group_name)
            if len(dirs) > 0:
                groups.extend(self.list_all_config_groups(group_name))
        return groups

    def format_config_groups(
        self, predicate: Callable[[str], bool], compact: bool = True
    ) -> str:
        groups = [x for x in self.list_all_config_groups() if predicate(x)]
        s = ""
        for group in sorted(groups):
            options = sorted(self.config_loader.get_group_options(group))
            if compact:
                items = ", ".join(options)
                line = "{}: {}".format(group, items)
            else:
                items = "\n".join(["  " + o for o in options])
                line = "{}:\n{}".format(group, items)
            s += line + "\n"

        return s

    def get_help(
        self, help_cfg: DictConfig, cfg: DictConfig, args_parser: ArgumentParser
    ) -> str:
        s = string.Template(help_cfg.template)
        help_text = s.substitute(
            FLAGS_HELP=self.format_args_help(args_parser),
            HYDRA_CONFIG_GROUPS=self.format_config_groups(
                lambda x: x.startswith("hydra/")
            ),
            APP_CONFIG_GROUPS=self.format_config_groups(
                lambda x: not x.startswith("hydra/")
            ),
            CONFIG=cfg.pretty(resolve=False),
        )
        return help_text

    def hydra_help(
        self, config_name: Optional[str], args_parser: ArgumentParser, args: Any
    ) -> None:
        cfg = self.compose_config(
            config_name=config_name,
            overrides=args.overrides,
            with_log_configuration=True,
        )
        help_cfg = cfg.hydra.hydra_help
        cfg = self.get_sanitized_hydra_cfg(cfg)
        help_text = self.get_help(help_cfg, cfg, args_parser)
        print(help_text)

    def app_help(
        self, config_name: Optional[str], args_parser: ArgumentParser, args: Any
    ) -> None:
        cfg = self.compose_config(
            config_name=config_name,
            overrides=args.overrides,
            with_log_configuration=True,
        )
        help_cfg = cfg.hydra.help
        clean_cfg = copy.deepcopy(cfg)
        with open_dict(clean_cfg):
            del clean_cfg["hydra"]
        help_text = self.get_help(help_cfg, clean_cfg, args_parser)
        print(help_text)

    @staticmethod
    def _log_header(header: str, prefix: str = "", filler: str = "-") -> None:
        assert log is not None
        log.debug(prefix + header)
        log.debug(prefix + "".ljust(len(header), filler))

    def _print_plugins(self) -> None:
        assert log is not None
        self._log_header(header="Installed Hydra Plugins", filler="*")
        all_plugins = {p.__name__ for p in Plugins.instance().discover()}
        for plugin_type in [
            ConfigSource,
            CompletionPlugin,
            Launcher,
            Sweeper,
            SearchPathPlugin,
        ]:
            # Mypy false positive?
            plugins = Plugins.instance().discover(plugin_type)  # type: ignore
            if len(plugins) > 0:
                Hydra._log_header(header=f"{plugin_type.__name__}:", prefix="\t")
                for plugin in plugins:
                    log.debug("\t\t{}".format(plugin.__name__))
                    all_plugins.remove(plugin.__name__)

        if len(all_plugins) > 0:
            Hydra._log_header(header="Generic plugins: ", prefix="\t")
            for plugin_name in all_plugins:
                log.debug("\t\t{}".format(plugin_name))

    def _print_search_path(self) -> None:
        assert log is not None
        log.debug("")
        self._log_header(header="Config search path", filler="*")

        box: List[List[str]] = [["Provider", "Search path"]]

        for sp in self.config_loader.get_sources():
            box.append([sp.provider, sp.full_path()])

        provider_pad, search_path_pad = get_column_widths(box)
        self._log_header(
            "| {} | {} |".format(
                "Provider".ljust(provider_pad), "Search path".ljust(search_path_pad)
            ),
            filler="-",
        )

        for source in self.config_loader.get_sources():
            log.debug(
                "| {} | {} |".format(
                    source.provider.ljust(provider_pad),
                    source.full_path().ljust(search_path_pad),
                )
            )

    def _print_composition_trace(self) -> None:
        # Print configurations used to compose the config object
        assert log is not None
        log.debug("")
        self._log_header("Composition trace", filler="*")
        box: List[List[str]] = [
            ["Config name", "Search path", "Provider", "Schema provider"]
        ]
        for trace in self.config_loader.get_load_history():
            box.append(
                [
                    trace.filename,
                    trace.path if trace.path is not None else "",
                    trace.provider if trace.provider is not None else "",
                    trace.schema_provider if trace.schema_provider is not None else "",
                ]
            )
        padding = get_column_widths(box)
        del box[0]

        self._log_header(
            "| {} | {} | {} | {} |".format(
                "Config name".ljust(padding[0]),
                "Search path".ljust(padding[1]),
                "Provider".ljust(padding[2]),
                "Schema provider".ljust(padding[3]),
            ),
            filler="-",
        )

        for row in box:
            log.debug(
                "| {} | {} | {} | {} |".format(
                    row[0].ljust(padding[0]),
                    row[1].ljust(padding[1]),
                    row[2].ljust(padding[2]),
                    row[3].ljust(padding[3]),
                )
            )

    def _print_plugins_profiling_info(self, top_n: int) -> None:
        assert log is not None
        stats = Plugins.instance().get_stats()
        if stats is None:
            return

        items = list(stats.modules_import_time.items())
        # hide anything that took less than 5ms
        filtered = filter(lambda x: x[1] > 0.0005, items)
        sorted_items = sorted(filtered, key=lambda x: x[1], reverse=True)

        top_n = max(len(sorted_items), top_n)
        box: List[List[str]] = [["Module", "Sec"]]

        for item in sorted_items[0:top_n]:
            box.append([item[0], f"{item[1]:.3f}"])
        padding = get_column_widths(box)

        log.debug("")
        self._log_header(header="Profiling information", filler="*")
        self._log_header(
            header=f"Total plugins scan time : {stats.total_time:.3f} seconds",
            filler="-",
        )

        self._log_header(
            f"| {box[0][0].ljust(padding[0])} | {box[0][1].ljust(padding[1])} |",
            filler="-",
        )
        del box[0]

        for row in box:
            a = row[0].ljust(padding[0])
            b = row[1].ljust(padding[1])
            log.debug(f"| {a} | {b} |")

    def _print_debug_info(self) -> None:
        assert log is not None
        if log.isEnabledFor(logging.DEBUG):
            self._print_plugins()
            self._print_search_path()
            self._print_composition_trace()
            self._print_plugins_profiling_info(10)

    def compose_config(
        self,
        config_name: Optional[str],
        overrides: List[str],
        strict: Optional[bool] = None,
        with_log_configuration: bool = False,
    ) -> DictConfig:
        """
        :param self:
        :param config_name:
        :param overrides:
        :param with_log_configuration: True to configure logging subsystem from the loaded config
        :param strict: None for default behavior (default to true for config file, false if no config file).
                       otherwise forces specific behavior.
        :return:
        """
        cfg = self.config_loader.load_configuration(
            config_name=config_name, overrides=overrides, strict=strict
        )
        with open_dict(cfg):
            from hydra import __version__

            cfg.hydra.runtime.version = __version__
            cfg.hydra.runtime.cwd = os.getcwd()
        if with_log_configuration:
            configure_log(cfg.hydra.hydra_logging, cfg.hydra.verbose)
            global log
            log = logging.getLogger(__name__)
            self._print_debug_info()
        return cfg
