# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import logging
import os
import string
from collections import defaultdict

import six
from omegaconf import open_dict, OmegaConf

from .config_loader import ConfigLoader
from .config_search_path import ConfigSearchPath
from .plugins import Plugins
from .utils import create_automatic_config_search_path, detect_task_name
from ..plugins import SearchPathPlugin, Launcher, Sweeper, CompletionPlugin
from ..plugins.common.utils import Singleton
from ..plugins.common.utils import (
    configure_log,
    run_job,
    JobRuntime,
    HydraConfig,
    setup_globals,
)

log = None


@six.add_metaclass(Singleton)
class GlobalHydra:
    def __init__(self):
        self.hydra = None

    def initialize(self, hydra):
        assert isinstance(hydra, Hydra)
        assert not self.is_initialized(), "GlobalHydra is already initialized"
        self.hydra = hydra

    def is_initialized(self):
        return self.hydra is not None

    def clear(self):
        self.hydra = None


class Hydra:
    @classmethod
    def create_main_hydra_file_or_module(
        cls, calling_file, calling_module, config_dir, strict
    ):
        config_search_path = create_automatic_config_search_path(
            calling_file, calling_module, config_dir
        )
        task_name = detect_task_name(calling_file, calling_module)
        return Hydra.create_main_hydra2(task_name, config_search_path, strict)

    @classmethod
    def create_main_hydra2(cls, task_name, config_search_path, strict):
        assert isinstance(config_search_path, ConfigSearchPath)

        config_loader = ConfigLoader(
            config_search_path=config_search_path, default_strict=strict
        )

        hydra = cls(task_name=task_name, config_loader=config_loader)
        GlobalHydra().initialize(hydra)
        return hydra

    def __init__(self, task_name, config_loader):
        """
        :param task_name: task name
        :param config_loader: config loader
        """
        setup_globals()
        self.config_loader = config_loader
        JobRuntime().set("name", task_name)

    def run(self, config_file, task_function, overrides):
        cfg = self.compose_config(
            config_file=config_file, overrides=overrides, with_log_configuration=True
        )
        HydraConfig().set_config(cfg)
        return run_job(
            config=cfg,
            task_function=task_function,
            job_dir_key="hydra.run.dir",
            job_subdir_key=None,
        )

    def multirun(self, config_file, task_function, overrides):
        # Initial config is loaded without strict (individual job configs may have strict).
        cfg = self.compose_config(
            config_file=config_file,
            overrides=overrides,
            strict=False,
            with_log_configuration=True,
        )
        HydraConfig().set_config(cfg)
        sweeper = Plugins.instantiate_sweeper(
            config=cfg, config_loader=self.config_loader, task_function=task_function
        )
        task_overrides = cfg.hydra.overrides.task
        return sweeper.sweep(arguments=task_overrides)

    @staticmethod
    def get_sanitized_hydra_cfg(src_cfg):
        cfg = copy.deepcopy(src_cfg)
        for key in list(cfg.keys()):
            if key != "hydra":
                del cfg[key]
        del cfg.hydra["hydra_help"]
        del cfg.hydra["help"]
        return cfg

    def show_cfg(self, config_file, overrides, cfg_type):
        assert cfg_type in ["job", "hydra", "all"]
        cfg = self.compose_config(
            config_file=config_file, overrides=overrides, with_log_configuration=True
        )
        if cfg_type == "job":
            del cfg["hydra"]
        elif cfg_type == "hydra":
            cfg = self.get_sanitized_hydra_cfg(cfg)
        print(cfg.pretty())

    @staticmethod
    def get_shell_to_plugin_map(config_loader):
        shell_to_plugin = defaultdict(list)
        for clazz in Plugins.discover(CompletionPlugin):
            plugin = clazz(config_loader)
            shell_to_plugin[plugin.provides()].append(plugin)

        for shell, plugins in shell_to_plugin.items():
            if len(plugins) > 1:
                raise ValueError(
                    "Multiple plugins installed for {} : {}".format(
                        shell, ",".join([type(plugin).__name__ for plugin in plugins])
                    )
                )

        return shell_to_plugin

    def shell_completion(self, config_file, overrides):
        subcommands = ["install", "uninstall", "query"]
        arguments = OmegaConf.from_dotlist(overrides)
        num_commands = sum(1 for key in subcommands if arguments[key] is not None)
        if num_commands != 1:
            raise ValueError(
                "Expecting one subcommand from {} to be set".format(subcommands)
            )

        shell_to_plugin = self.get_shell_to_plugin_map(self.config_loader)

        def find_plugin(cmd):
            if cmd not in shell_to_plugin:
                raise ValueError(
                    "No completion plugin for '{}' found, available : \n{}".format(
                        cmd, "\n".join(["\t" + x for x in shell_to_plugin.keys()])
                    )
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
            plugin.query(config_file=config_file)

    @staticmethod
    def format_args_help(args_parser):
        s = ""
        overrides = None
        for action in args_parser._actions:
            if len(action.option_strings) == 0:
                overrides = action
            else:
                s += "{} : {}\n".format(",".join(action.option_strings), action.help)
        s += "Overrides : " + overrides.help
        return s

    def list_all_config_groups(self, parent=""):
        groups = []
        for group in self.config_loader.list_groups(parent):
            if parent == "":
                group_name = group
            else:
                group_name = "{}/{}".format(parent, group)
            files = self.config_loader.get_group_options(group_name, file_type="file")
            dirs = self.config_loader.get_group_options(group_name, file_type="dir")
            if len(files) > 0:
                groups.append(group_name)
            if len(dirs) > 0:
                groups.extend(self.list_all_config_groups(group_name))
        return groups

    def format_config_groups(self, predicate, compact=True):
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

    def get_help(self, help_cfg, cfg, args_parser):
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

    def hydra_help(self, config_file, args_parser, args):
        cfg = self.compose_config(
            config_file=config_file,
            overrides=args.overrides,
            with_log_configuration=True,
        )
        help_cfg = cfg.hydra.hydra_help
        cfg = self.get_sanitized_hydra_cfg(cfg)
        help_text = self.get_help(help_cfg, cfg, args_parser)
        print(help_text)

    def app_help(self, config_file, args_parser, args):
        cfg = self.compose_config(
            config_file=config_file,
            overrides=args.overrides,
            with_log_configuration=True,
        )
        help_cfg = cfg.hydra.help
        clean_cfg = copy.deepcopy(cfg)
        del clean_cfg["hydra"]
        help_text = self.get_help(help_cfg, clean_cfg, args_parser)
        print(help_text)

    @staticmethod
    def _log_header(header, prefix="", filler="-"):
        log.debug(prefix + header)
        log.debug(prefix + "".ljust(len(header), filler))

    def _print_plugins(self):
        self._log_header(header="Installed Hydra Plugins", filler="*")
        for plugin_type in [SearchPathPlugin, Sweeper, Launcher]:
            Hydra._log_header(
                header="{}:".format(plugin_type.__name__), prefix="\t", filler="-"
            )
            for plugin in Plugins.discover(plugin_type):
                log.debug("\t\t{}".format(plugin.__name__))

    def _get_padding(self):
        provider_pad = 0
        search_path_pad = 0
        file_pad = 0
        for sp in self.config_loader.config_search_path.config_search_path:
            provider_pad = max(provider_pad, len(sp.provider))
            search_path_pad = max(search_path_pad, len(sp.path))
        for file, _, _ in self.config_loader.get_load_history():
            file_pad = max(file_pad, len(file))

        provider_pad += 1
        search_path_pad += 1
        file_pad += 1
        return provider_pad, search_path_pad, file_pad

    def _print_search_path(self):
        log.debug("")
        self._log_header(header="Hydra config search path", filler="*")

        provider_pad, search_path_pad, file_pad = self._get_padding()
        self._log_header(
            "| {} | {} |".format(
                "Provider".ljust(provider_pad), "Search path".ljust(search_path_pad)
            ),
            filler="-",
        )

        for sp in self.config_loader.config_search_path.config_search_path:
            log.debug(
                "| {} | {} |".format(
                    sp.provider.ljust(provider_pad), sp.path.ljust(search_path_pad)
                )
            )

    def _print_composition_trace(self):
        # Print configurations used to compose the config object
        provider_pad, search_path_pad, file_pad = self._get_padding()
        log.debug("")
        self._log_header("Composition trace", filler="*")
        self._log_header(
            "| {} | {} | {} |".format(
                "Provider".ljust(provider_pad),
                "Search path".ljust(search_path_pad),
                "File".ljust(file_pad),
            ),
            filler="-",
        )

        for file, search_path, provider in self.config_loader.get_load_history():
            if search_path is not None:
                log.debug(
                    "| {} | {} | {} |".format(
                        provider.ljust(provider_pad),
                        search_path.ljust(search_path_pad),
                        file.ljust(file_pad),
                    )
                )
            else:
                log.debug("{} : NOT FOUND".format(file))

    def _print_debug_info(self):
        self._print_plugins()
        self._print_search_path()
        self._print_composition_trace()

    def compose_config(
        self, config_file, overrides, strict=None, with_log_configuration=False
    ):
        """
        :param self:
        :param config_file:
        :param overrides:
        :param with_log_configuration: True to configure logging subsystem from the loaded config
        :param strict: None for default behavior (default to true for config file, false if no config file).
                       otherwise forces specific behavior.
        :return:
        """
        cfg = self.config_loader.load_configuration(
            config_file=config_file, overrides=overrides, strict=strict
        )
        with open_dict(cfg):
            from .. import __version__

            cfg.hydra.runtime.version = __version__
            cfg.hydra.runtime.cwd = os.getcwd()
        if with_log_configuration:
            configure_log(cfg.hydra.hydra_logging, cfg.hydra.verbose)
            global log
            log = logging.getLogger(__name__)
            self._print_debug_info()
        return cfg
