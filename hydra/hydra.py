import argparse
import itertools
import logging
import logging.config
import os
import sys
from time import strftime, localtime

import pkg_resources
from omegaconf import OmegaConf

from hydra import utils, Task

# add cwd to path to allow running directly from the repo top level directory
sys.path.append(os.getcwd())

log = None


def configure_log(cfg_dir, cfg, verbose=None):
    """
    :param cfg:
    :param verbose: all or root to activate verbose logging for all modules, otherwise a comma separated list of modules
    :return:
    """
    # configure target directory for all logs files (binary, text. models etc)
    log_dir_suffix = cfg.log_dir_suffix or strftime("%Y-%m-%d_%H-%M-%S", localtime())
    log_dir = os.path.join(cfg.log_dir or "logs", log_dir_suffix)
    cfg.full_log_dir = log_dir
    os.makedirs(cfg.full_log_dir, exist_ok=True)

    logging_config = cfg.logging.config
    if not os.path.isabs(logging_config):
        logging_config = os.path.join(cfg_dir, logging_config)

    logcfg = OmegaConf.from_filename(logging_config)
    log_name = logcfg.handlers.file.filename
    if not os.path.isabs(log_name):
        logcfg.handlers.file.filename = os.path.join(cfg.full_log_dir, log_name)
    logging.config.dictConfig(logcfg.to_dict())

    global log
    log = logging.getLogger(__name__)

    if verbose:
        if verbose == 'root':
            logging.getLogger().setLevel(logging.DEBUG)
        for logger in verbose.split(','):
            logging.getLogger(logger).setLevel(logging.DEBUG)

    log.info(f"Saving logs to {cfg.full_log_dir}")


def get_args():
    parser = argparse.ArgumentParser(description='Hydra experimentation framework')
    version = pkg_resources.require("hydra")[0].version
    parser.add_argument('--version', action='version', version=f"hydra {version}")

    subparsers = parser.add_subparsers(help="sub-command help", dest="command")
    run_parser = subparsers.add_parser("run", help="Run a task")
    run_parser.add_argument(
        help="Task directory or name",
        type=str,
        dest="task"
    )

    # parser.add_argument('--log_config', '-l', help='Log configuration file', default=None)
    parser.add_argument('--verbose', '-v',
                        help='Activate debug logging, otherwise takes a '
                             'comma separated list of loggers ("root" for root logger)',
                        nargs='?',
                        default='')

    run_parser.add_argument('--presets', '-p', nargs='*')
    run_parser.add_argument('--overrides', '-o', nargs='*')

    return parser.parse_args()


def find_task(task_class):
    return utils.get_class(task_class)()


def find_cfg_dir(task_class):
    path = os.getcwd()
    paths = [path]
    for p in task_class.split('.'):
        path = os.path.realpath(os.path.join(path, p))
        paths.append(path)

    for p in reversed(paths):
        path = os.path.join(p, 'conf')
        if os.path.exists(p) and os.path.isdir(path):
            return path


def create_task_cfg(cfg_dir, args):
    task_name = args.task.split('.')[-1]
    cfg = OmegaConf.from_filename(os.path.join(cfg_dir, "{}.yaml".format(task_name)))

    for preset in args.presets or {}:
        key, value = preset.split('=')
        cfg.presets[key] = value

    presets_list = cfg.get('presets', {}).items()
    for combo in list(itertools.product(presets_list, presets_list)):
        if combo[0] != combo[1]:
            path = os.path.join(cfg_dir, combo[0][0], combo[0][1], combo[1][0], combo[1][1]) + '.yaml'
            if os.path.exists(path):
                cfg = OmegaConf.merge(cfg, OmegaConf.from_filename(path))

    cfg = OmegaConf.merge(cfg, OmegaConf.from_cli(args.overrides or []))
    return cfg


def main():
    args = get_args()
    print(args)
    if args.command == 'run':
        cfg_dir = find_cfg_dir(args.task)
        cfg = create_task_cfg(cfg_dir, args)
        configure_log(cfg_dir, cfg, args.verbose)

        task = find_task(args.task)
        assert isinstance(task, Task)

        task.setup(cfg=cfg, log=log)
        task.run(cfg=cfg)


if __name__ == '__main__':
    main()
