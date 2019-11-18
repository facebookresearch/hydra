# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import logging
import os
import re
import sys
from os.path import dirname, splitext, basename
from time import strftime, localtime

import six
from omegaconf import OmegaConf, DictConfig, ListConfig

from hydra._internal.pathlib import Path

# pylint: disable=C0103
log = logging.getLogger(__name__)


def configure_log(log_config, verbose_config):
    assert isinstance(verbose_config, (bool, str, ListConfig))
    if log_config is not None:
        conf = OmegaConf.to_container(log_config, resolve=True)
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
    if isinstance(verbose_config, bool):
        if verbose_config:
            logging.getLogger().setLevel(logging.DEBUG)
    else:
        if isinstance(verbose_config, str):
            verbose_config = OmegaConf.create([verbose_config])
        for logger in verbose_config:
            logging.getLogger(logger).setLevel(logging.DEBUG)


def _save_config(cfg, filename, output_dir):
    Path(str(output_dir)).mkdir(parents=True, exist_ok=True)
    with open(str(output_dir / filename), "w") as file:
        file.write(cfg.pretty())


def get_overrides_dirname(input_list, exclude_keys=[], item_sep=",", kv_sep="="):
    lst = []
    for x in input_list:
        key, _val = split_key_val(x)
        if key not in exclude_keys:
            lst.append(x)

    lst.sort()
    # TODO? what is this re doing?
    return re.sub(pattern="[=]", repl=kv_sep, string=item_sep.join(lst))


def filter_overrides(overrides):
    """
    :param overrides: overrides list
    :return: returning a new overrides list with all the keys starting with hydra. filtered.
    """
    return [x for x in overrides if not x.startswith("hydra.")]


def split_key_val(s):
    assert "=" in s, "'{}' not a valid override, expecting key=value format".format(s)

    idx = s.find("=")
    assert idx != -1
    return s[0:idx], s[idx + 1 :]


def run_job(config, task_function, job_dir_key, job_subdir_key):
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
        ret.overrides = OmegaConf.to_container(config.hydra.overrides.task)
        # handle output directories here
        Path(str(working_dir)).mkdir(parents=True, exist_ok=True)
        os.chdir(working_dir)
        hydra_output = Path(config.hydra.output_subdir)

        configure_log(config.hydra.job_logging, config.hydra.verbose)

        # TODO: update this after https://github.com/omry/omegaconf/issues/42 is resolved
        hydra_cfg = OmegaConf.create({"hydra": config["hydra"]})

        _save_config(task_cfg, "config.yaml", hydra_output)
        _save_config(hydra_cfg, "hydra.yaml", hydra_output)
        _save_config(config.hydra.overrides.task, "overrides.yaml", hydra_output)
        ret.return_value = task_function(task_cfg)
        ret.task_name = JobRuntime().get("name")
        return ret
    finally:
        os.chdir(old_cwd)


def get_valid_filename(s):
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def setup_globals():
    try:
        OmegaConf.register_resolver(
            "now", lambda pattern: strftime(pattern, localtime())
        )
    except AssertionError:
        # calling it again in no_workers mode will throw. safe to ignore.
        pass


class JobReturn:
    def __init__(self):
        self.overrides = None
        self.return_value = None
        self.cfg = None
        self.hydra_cfg = None
        self.working_dir = None
        self.task_name = None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @staticmethod
    def get_state():
        return Singleton._instances

    @staticmethod
    def set_state(instances):
        Singleton._instances = instances


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


def split_config_path(config_path):
    if config_path is None or config_path == "":
        return None, None
    split_file = splitext(config_path)
    if split_file[1] in (".yaml", ".yml"):
        # assuming dir/config.yaml form
        config_file = basename(config_path)
        config_dir = dirname(config_path)
    else:
        # assuming dir form without a config file.
        config_file = None
        config_dir = config_path

    if config_dir == "":
        config_dir = None

    if config_file == "":
        config_file = None
    return config_dir, config_file
