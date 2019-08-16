import copy
import inspect
import logging
import logging.config
import os
import re
import sys
from time import strftime, localtime

import six
from omegaconf import OmegaConf, DictConfig

# pylint: disable=C0103
log = logging.getLogger(__name__)


def get_valid_filename(s):
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def setup_globals():
    try:
        OmegaConf.register_resolver(
            "now", lambda pattern: strftime(pattern, localtime())
        )

        def job_error(x):
            raise Exception(
                "job:{} is no longer available. use hydra.job.{}".format(x, x)
            )

        OmegaConf.register_resolver("job", job_error)

    except AssertionError:
        # calling it again in no_workers mode will throw. safe to ignore.
        pass


def run_job(config, task_function, verbose, job_dir_key, job_subdir_key):
    old_cwd = os.getcwd()
    working_dir = str(config.select(job_dir_key))
    if job_subdir_key is not None:
        # evaluate job_subdir_key lazily.
        # this is running on the client side in sweep and contains things such as job:id which
        # are only available there.
        subdir = str(config.select(job_subdir_key))
        working_dir = os.path.join(working_dir, subdir)

    try:
        ret = JobReturn()
        ret.working_dir = working_dir
        task_cfg = copy.deepcopy(config)
        del task_cfg["hydra"]
        ret.cfg = task_cfg
        ret.hydra_cfg = copy.deepcopy(HydraConfig())
        ret.overrides = config.hydra.overrides.task.to_container()
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        os.chdir(working_dir)
        configure_log(config.hydra.job_logging, verbose)

        save_config(task_cfg, "config.yaml")
        save_config(config.hydra.overrides.task, "overrides.yaml")
        ret.return_value = task_function(task_cfg)
        return ret
    finally:
        os.chdir(old_cwd)


def filter_overrides(overrides):
    """
    :param overrides: overrides list
    :return: returning a new overrides list with all the keys starting with hydra. fitlered.
    """
    return [x for x in overrides if not x.startswith("hydra.")]


def get_overrides_dirname(lst, exclude_keys=[]):
    lst = [x for x in lst if x not in exclude_keys]
    lst.sort()
    return re.sub(pattern="[=]", repl=":", string=",".join(lst))


def save_config(cfg, filename):
    with open(os.path.join(filename), "w") as file:
        file.write(cfg.pretty())


def configure_log(log_config, verbose=None):
    if log_config is not None:
        conf = log_config.to_container(resolve=True)
        logging.config.dictConfig(conf)
    else:
        # default logging to stdout
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s][%(name)s][%(levelname)s] - %(message)s"
        )
        handler.setFormatter(formatter)
        root.addHandler(handler)

    if verbose is not None:
        if verbose == "root":
            logging.getLogger().setLevel(logging.DEBUG)
        for logger in verbose.split(","):
            logging.getLogger(logger).setLevel(logging.DEBUG)


class JobReturn:
    def __init__(self):
        self.overrides = None
        self.return_value = None
        self.cfg = None
        self.hydra_cfg = None
        self.working_dir = None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@six.add_metaclass(Singleton)
class JobRuntime:
    def __init__(self):
        self.conf = OmegaConf.create()
        self.set("name", "UNKNOWN_NAME")

    def get(self, key):
        ret = self.conf.select(key)
        if ret is None:
            raise KeyError("Key not found in {}: {}".format(type(self).__name__, key))
        return ret

    def set(self, key, value):
        log.debug("Setting {}:{}={}".format(type(self).__name__, key, value))
        self.conf[key] = value


@six.add_metaclass(Singleton)
class HydraConfig(DictConfig):
    def __init__(self):
        super(HydraConfig, self).__init__(content={})
        self.hydra = None

    def set_config(self, cfg):
        try:
            OmegaConf.set_readonly(self, False)
            self.hydra = copy.deepcopy(cfg.hydra)
        finally:
            OmegaConf.set_readonly(self, True)


def run_hydra(args, task_function, config_path, strict):
    stack = inspect.stack()
    calling_file = stack[2][0].f_locals["__file__"]

    target_file = os.path.basename(calling_file)
    task_name = os.path.splitext(target_file)[0]

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

    from .hydra import Hydra

    hydra = Hydra(
        task_name=task_name,
        conf_dir=conf_dir,
        conf_filename=conf_filename,
        task_function=task_function,
        verbose=args.verbose,
        strict=strict,
    )

    if args.run + args.cfg + args.multirun > 1:
        raise ValueError("Only one of --run, --sweep and --cfg can be specified")
    if args.run + args.cfg + args.multirun == 0:
        args.run = True

    if args.run:
        command = "run"
    elif args.sweep:
        raise RuntimeError("-s|--sweep is no longer supported, please us -m|--multirun")
    elif args.multirun:
        command = "multirun"
    elif args.cfg:
        command = "cfg"

    if command == "run":
        hydra.run(overrides=args.overrides)
    elif command == "multirun":
        hydra.multirun(overrides=args.overrides)
    elif command == "cfg":
        hydra.show_cfg(overrides=args.overrides)
    else:
        print("Command not specified")
