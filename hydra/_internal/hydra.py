# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
from os.path import realpath, dirname, splitext, basename

from omegaconf import open_dict
from collections import defaultdict
from .config_loader import ConfigLoader
from .config_search_path import ConfigSearchPath
from .plugins import Plugins
from ..errors import MissingConfigException
from ..plugins import SearchPathPlugin, Launcher, Sweeper, CompletionPlugin
from ..plugins.common.utils import (
    configure_log,
    run_job,
    get_valid_filename,
    JobRuntime,
    HydraConfig,
    setup_globals,
    get_overrides_dirname,
)

log = None


class Hydra:
    def __init__(
        self, calling_file, calling_module, config_path, task_function, verbose, strict
    ):
        setup_globals()

        assert calling_module is not None or calling_file is not None
        basedir_prefix = ""
        if calling_module is None:
            # executed with python file.py
            abs_base_dir = realpath(dirname(calling_file))
            target_file = os.path.basename(calling_file)
            task_name = os.path.splitext(target_file)[0]
        else:
            # module is installed, use pkg:// access to get configs
            last_dot = calling_module.rfind(".")
            if last_dot != -1:
                task_name = calling_module[last_dot + 1 :]
            else:
                task_name = calling_module
            basedir_prefix = "pkg://"
            abs_base_dir = calling_module

        JobRuntime().set("name", get_valid_filename(task_name))
        self.task_name = task_name
        self.task_function = task_function

        split_file = splitext(config_path)
        if split_file[1] in (".yaml", ".yml"):
            # assuming dir/config.yaml form
            config_file = basename(config_path)
            config_dir = dirname(config_path)
        else:
            # assuming dir form without a config file.
            config_file = None
            config_dir = config_path

        if config_dir != "":
            abs_config_dir = "{}/{}".format(abs_base_dir, config_dir)
        else:
            abs_config_dir = abs_base_dir

        abs_config_dir = basedir_prefix + abs_config_dir

        search_path = ConfigSearchPath()
        search_path.append("hydra", "pkg://hydra.conf")
        search_path.append("main", abs_config_dir)

        search_path_plugins = Plugins.discover(SearchPathPlugin)
        for spp in search_path_plugins:
            plugin = spp()
            plugin.manipulate_search_path(search_path)

        self.config_loader = ConfigLoader(
            config_file=config_file, config_search_path=search_path, strict_cfg=strict
        )

        if not self.config_loader.exists(abs_config_dir):
            raise MissingConfigException(
                missing_cfg_file=abs_config_dir,
                message="Primary config dir not found: {}".format(abs_config_dir),
            )

        if config_file is not None and not self.config_loader.exists_in_search_path(
            config_file
        ):
            raise MissingConfigException(
                missing_cfg_file=config_file,
                message="Cannot find primary config file: {}".format(config_file),
            )
        self.verbose = verbose

    def run(self, overrides):
        cfg = self._load_config(overrides)
        HydraConfig().set_config(cfg)
        with open_dict(cfg):
            cfg.hydra.job.override_dirname = get_overrides_dirname(
                cfg.hydra.overrides.task
            )

        return run_job(
            config=cfg,
            task_function=self.task_function,
            verbose=self.verbose,
            job_dir_key="hydra.run.dir",
            job_subdir_key=None,
        )

    def multirun(self, overrides):
        cfg = self._load_config(overrides)
        HydraConfig().set_config(cfg)
        sweeper = Plugins.instantiate_sweeper(
            config=cfg,
            config_loader=self.config_loader,
            task_function=self.task_function,
            verbose=self.verbose,
        )
        task_overrides = cfg.hydra.overrides.task
        return sweeper.sweep(arguments=task_overrides)

    def show_cfg(self, overrides):
        config = self._load_config(overrides)
        log.info("\n" + config.pretty())

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

    def shell_completion(self, overrides):
        config = self._load_config(overrides)
        subcommands = ["install", "uninstall", "query"]
        found = False
        for sc in subcommands:
            if sc in config:
                found = True
                break
        if not found:
            log.error(
                "No completion subcommand specified ({})".format(",".join(subcommands))
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

        if config.install:
            plugin = find_plugin(config.install)
            plugin.install()
        elif config.uninstall:
            plugin = find_plugin(config.uninstall)
            plugin.uninstall()
        elif config.query:
            plugin = find_plugin(config.query)
            plugin.query()

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

    def _load_config(self, overrides):
        cfg = self.config_loader.load_configuration(overrides)
        configure_log(cfg.hydra.hydra_logging, self.verbose)
        global log
        log = logging.getLogger(__name__)
        self._print_debug_info()
        return cfg
