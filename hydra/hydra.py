import inspect
import os
import sys
import traceback

import argparse
import pkg_resources
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


def run_hydra(task_function, config_path):
    stack = inspect.stack()
    calling_file = stack[2][0].f_locals['__file__']
    utils.setup_globals()
    args = get_args()

    if os.path.isabs(config_path):
        raise RuntimeError("Config path should be relative")
    conf_file = os.path.realpath(os.path.join(os.path.dirname(calling_file), config_path))
    conf_dir = os.path.dirname(conf_file)
    conf_filename = os.path.basename(conf_file)

    if args.command == 'run':
        hydra_cfg = utils.create_hydra_cfg(cfg_dir=conf_dir, overrides=args.overrides)
        utils.run_job(cfg_dir=conf_dir,
                      cfg_filename=conf_filename,
                      hydra_cfg=hydra_cfg,
                      task_function=task_function,
                      overrides=args.overrides,
                      verbose=args.verbose,
                      workdir=hydra_cfg.hydra.run_dir)
    elif args.command == 'cfg':
        hydra_cfg = utils.create_hydra_cfg(cfg_dir=conf_dir, overrides=args.overrides)
        task_cfg = utils.create_task_cfg(cfg_dir=conf_dir,
                                         cfg_filename=conf_filename,
                                         cli_overrides=args.overrides)
        job_cfg = task_cfg['cfg']
        if args.config == 'job':
            cfg = job_cfg
        elif args.config == 'hydra':
            cfg = hydra_cfg
        elif args.config == 'both':
            cfg = OmegaConf.merge(hydra_cfg, job_cfg)
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
        hydra_cfg = utils.create_hydra_cfg(cfg_dir=conf_dir, overrides=args.overrides)
        launcher = FAIRTaskLauncher(cfg_dir=conf_dir,
                                    cfg_filename=conf_filename,
                                    hydra_cfg=hydra_cfg,
                                    task_function=task_function,
                                    overrides=args.overrides)
        launcher.launch()

    else:
        print("Command not specified")


def main(config_path):
    def main_decorator(task_function):
        def decorated_main():
            try:
                run_hydra(task_function, config_path)
            except KeyboardInterrupt:
                sys.exit(-1)
            except SystemExit:
                pass
            # noinspection PyBroadException
            except Exception:
                cla, exc, trbk = sys.exc_info()
                sys.stderr.write(
                    "Caught Exception:\n%s:%s\n%s" % (cla.__name__, str(exc), ''.join(traceback.format_tb(trbk, 5))))
                sys.exit(-1)

        return decorated_main

    return main_decorator
