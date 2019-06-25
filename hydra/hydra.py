import copy
import inspect
import os
import sys
import traceback

import argparse
import pkg_resources
import re
from omegaconf import OmegaConf

from hydra.fairtask_launcher import FAIRTaskLauncher
from . import utils


def get_args():
    parser = argparse.ArgumentParser(description='Hydra experimentation framework')
    version = pkg_resources.require("hydra")[0].version
    parser.add_argument('--version', action='version', version="hydra {}".format(version))

    def add_default_switches(prs):
        prs.add_argument('overrides', nargs='*', help="Any key=value arguments to override config values "
                                                      "(use dots for.nested=overrides)")

    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    parser.add_argument('--verbose', '-v',
                        help='Activate debug logging, otherwise takes a '
                             'comma separated list of loggers ("root" for root logger)',
                        nargs='?',
                        default='')

    cfg_parser = subparsers.add_parser("cfg", help="Show generated cfg")
    add_default_switches(cfg_parser)

    cfg_parser.add_argument('--config', '-c',
                            help='type of config',
                            choices=['job', 'hydra', 'both'],
                            default='job')

    cfg_parser.add_argument('--debug', '-d', action="store_true", default=False,
                            help="Show how the config was generated")

    run_parser = subparsers.add_parser("run", help="Run a task")
    add_default_switches(run_parser)

    sweep_parser = subparsers.add_parser("sweep", help="Run a parameter sweep")
    add_default_switches(sweep_parser)

    return parser.parse_args()


class Hydra:

    def __init__(self,
                 task_name,
                 conf_dir,
                 conf_filename,
                 task_function,
                 verbose):
        # clear the resolvers cache. this is useful for unit tests
        OmegaConf.clear_resolvers()
        utils.setup_globals()
        self.task_name = utils.get_valid_filename(task_name)
        self.conf_dir = conf_dir
        self.conf_filename = conf_filename
        self.task_function = task_function
        self.verbose = verbose

    def run(self, overrides):
        overrides = copy.deepcopy(overrides)
        hydra_cfg = utils.create_hydra_cfg(
            task_name=self.task_name,
            cfg_dir=self.conf_dir,
            overrides=overrides)
        utils.run_job(cfg_dir=self.conf_dir,
                      cfg_filename=self.conf_filename,
                      hydra_cfg=hydra_cfg,
                      task_function=self.task_function,
                      overrides=overrides,
                      verbose=self.verbose,
                      workdir=hydra_cfg.hydra.run_dir)

    def sweep(self, overrides):
        hydra_cfg = utils.create_hydra_cfg(
            task_name=self.task_name,
            cfg_dir=self.conf_dir,
            overrides=overrides)

        launcher = FAIRTaskLauncher(cfg_dir=self.conf_dir,
                                    cfg_filename=self.conf_filename,
                                    hydra_cfg=hydra_cfg,
                                    task_function=self.task_function,
                                    overrides=overrides)

        launcher.launch()

    def get_cfg(self, overrides):
        overrides = copy.deepcopy(overrides)
        hydra_cfg = utils.create_hydra_cfg(
            task_name=self.task_name,
            cfg_dir=self.conf_dir,
            overrides=overrides)
        ret = utils.create_task_cfg(cfg_dir=self.conf_dir,
                                    cfg_filename=self.conf_filename,
                                    cli_overrides=overrides)
        ret['hydra_cfg'] = hydra_cfg
        return ret


def run_hydra(task_function, config_path):
    stack = inspect.stack()
    calling_file = stack[2][0].f_locals['__file__']

    target_file = os.path.basename(calling_file)
    task_name = os.path.splitext(target_file)[0]  # TODO: this should only replace hydra.name if it's '???'

    args = get_args()

    if os.path.isabs(config_path):
        raise RuntimeError("Config path should be relative")
    abs_config_path = os.path.realpath(os.path.join(os.path.dirname(calling_file), config_path))
    if not os.path.exists(abs_config_path):
        raise RuntimeError("Config path '{}' does not exist".format(abs_config_path))
    if os.path.isfile(abs_config_path):
        conf_dir = os.path.dirname(abs_config_path)
        conf_filename = os.path.basename(abs_config_path)
    else:
        conf_dir = abs_config_path
        conf_filename = None

    hydra = Hydra(task_name=task_name,
                  conf_dir=conf_dir,
                  conf_filename=conf_filename,
                  task_function=task_function,
                  verbose=args.verbose)

    if args.command == 'run':
        hydra.run(overrides=args.overrides)
    elif args.command == 'cfg':
        task_cfg = hydra.get_cfg(overrides=args.overrides)
        job_cfg = task_cfg['cfg']
        if args.config == 'job':
            cfg = job_cfg
        elif args.config == 'hydra':
            cfg = task_cfg['hydra_cfg']
        elif args.config == 'both':
            cfg = OmegaConf.merge(task_cfg['hydra_cfg'], job_cfg)
        else:
            assert False
        if args.debug:
            for file, loaded in task_cfg['checked']:
                if loaded:
                    print("Loaded: {}".format(file))
                else:
                    print("Not found: {}".format(file))

        print(cfg.pretty())
    elif args.command == 'sweep':
        hydra.sweep(overrides=args.overrides)
    else:
        print("Command not specified")


def main(config_path="."):
    def main_decorator(task_function):
        def decorated_main():
            try:
                run_hydra(task_function, config_path)
            except KeyboardInterrupt:
                sys.exit(-1)
            except SystemExit:
                pass

        return decorated_main

    return main_decorator
