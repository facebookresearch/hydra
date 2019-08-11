# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
import logging
import os
import sys

import argparse
import pkg_resources

from . import utils
from .config_loader import ConfigLoader
from .plugins import Plugins
from .utils import JobRuntime, HydraConfig


def get_args():
    parser = argparse.ArgumentParser(description="Hydra experimentation framework")
    version = pkg_resources.require("hydra")[0].version
    parser.add_argument(
        "--version", action="version", version="hydra {}".format(version)
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
    parser.add_argument("--sweep", "-s", action="store_true", help="Perform a sweep")

    return parser.parse_args()


def print_load_history(loader):
    for file, loaded in loader.get_load_history():
        if loaded:
            log.debug("Loaded: {}".format(file))
        else:
            log.debug("Not found: {}".format(file))


class Hydra:
    def __init__(
        self, task_name, conf_dir, conf_filename, task_function, verbose, strict
    ):
        utils.setup_globals()
        JobRuntime().set("name", utils.get_valid_filename(task_name))
        self.task_name = task_name
        self.conf_dir = conf_dir
        self.conf_filename = conf_filename
        self.task_function = task_function
        self.config_loader = ConfigLoader(
            conf_dir=self.conf_dir,
            conf_filename=self.conf_filename,
            strict_task_cfg=strict,
        )
        self.verbose = verbose

    def run(self, overrides):
        cfg = self.load_config(overrides)
        HydraConfig().set_config(cfg)
        return utils.run_job(
            config=cfg,
            task_function=self.task_function,
            verbose=self.verbose,
            job_dir_key="hydra.run.dir",
            job_subdir_key=None,
        )

    def sweep(self, overrides):
        cfg = self.load_config(overrides)
        HydraConfig().set_config(cfg)
        sweeper = Plugins.instantiate_sweeper(
            config=cfg,
            config_loader=self.config_loader,
            task_function=self.task_function,
            verbose=self.verbose,
        )
        return sweeper.sweep(arguments=cfg.hydra.overrides.task)

    def load_config(self, overrides):
        cfg = self.config_loader.load_configuration(overrides)
        utils.configure_log(cfg.hydra.hydra_logging, self.verbose)
        global log
        log = logging.getLogger(__name__)
        print_load_history(self.config_loader)
        return cfg


def run_hydra(task_function, config_path, strict):
    stack = inspect.stack()
    calling_file = stack[2][0].f_locals["__file__"]

    target_file = os.path.basename(calling_file)
    task_name = os.path.splitext(target_file)[0]
    args = get_args()

    if os.path.isabs(config_path):
        raise RuntimeError("Config path should be relative")
    abs_config_path = os.path.realpath(
        os.path.join(os.path.dirname(calling_file), config_path)
    )
    if not os.path.exists(abs_config_path):
        raise RuntimeError("Config path '{}' does not exist".format(abs_config_path))
    if os.path.isfile(abs_config_path):
        conf_dir = os.path.dirname(abs_config_path)
        conf_filename = os.path.basename(abs_config_path)
    else:
        conf_dir = abs_config_path
        conf_filename = None

    hydra = Hydra(
        task_name=task_name,
        conf_dir=conf_dir,
        conf_filename=conf_filename,
        task_function=task_function,
        verbose=args.verbose,
        strict=strict,
    )

    if args.run + args.cfg + args.sweep > 1:
        raise ValueError("Only one of --run, --sweep and --cfg can be specified")
    if args.run + args.cfg + args.sweep == 0:
        args.run = True

    if args.run:
        command = "run"
    elif args.sweep:
        command = "sweep"
    elif args.cfg:
        command = "cfg"

    if command == "run":
        hydra.run(overrides=args.overrides)
    elif command == "sweep":
        hydra.sweep(overrides=args.overrides)
    elif command == "cfg":
        config = hydra.load_config(args.overrides)
        log.info("\n" + config.pretty())
    else:
        print("Command not specified")


def main(config_path=".", strict=False):
    """
    :param config_path: the config path, can be a directory in which it's used as the config root
    or a file to load
    :param strict: strict mode, will throw an error if command line overrides are not changing an
    existing key or
           if the code is accessing a non existent key
    """

    def main_decorator(task_function):
        def decorated_main():
            try:
                run_hydra(task_function, config_path, strict)
            except KeyboardInterrupt:
                sys.exit(-1)
            except SystemExit:
                pass

        return decorated_main

    return main_decorator
