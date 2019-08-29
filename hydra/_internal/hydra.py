# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
from os.path import realpath, dirname, splitext, basename

from omegaconf import open_dict

from .config_loader import ConfigLoader
from .plugins import Plugins
from ..errors import MissingConfigException
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
                calling_module = calling_module[0:last_dot]
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

        abs_config_dir = basedir_prefix + "{}/{}".format(abs_base_dir, config_dir)
        self.config_loader = ConfigLoader(
            config_file=config_file,
            job_search_path=[abs_config_dir],
            hydra_search_path=["pkg://hydra.conf"],
            strict_cfg=strict,
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

    def _load_config(self, overrides):
        cfg = self.config_loader.load_configuration(overrides)
        configure_log(cfg.hydra.hydra_logging, self.verbose)
        global log
        log = logging.getLogger(__name__)
        self._print_debug_info(cfg)
        return cfg

    def _print_debug_info(self, cfg):
        log.debug("Hydra config search path:")
        for path in self.config_loader.get_hydra_search_path():
            log.debug("\t" + path)
        log.debug("")
        log.debug("Job config search path:")
        for path in self.config_loader.get_job_search_path():
            log.debug("\t" + path)
        log.debug("")
        for file, loaded in self.config_loader.get_load_history():
            if loaded:
                log.debug("Loaded: {}".format(file))
            else:
                log.debug("Not found: {}".format(file))
