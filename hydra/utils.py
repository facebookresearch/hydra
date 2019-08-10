# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import inspect
import itertools
import logging
import logging.config
import os
import re
import sys
from time import strftime, localtime

from omegaconf import OmegaConf

# pylint: disable=C0103
log = logging.getLogger(__name__)


def singleton(class_):
    instances = {}

    def instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return instance


class RuntimeVariables:
    def __init__(self):
        self.conf = OmegaConf.create()

    def get(self, key):
        ret = self.conf.select(key)
        if ret is None:
            raise KeyError(
                "Key not found in {}: {}".format(
                    type(self).__name__, key))
        return ret

    def set(self, key, value):
        log.debug("Setting {}:{}={}".format(type(self).__name__, key, value))
        self.conf[key] = value


@singleton
class JobRuntime(RuntimeVariables):
    pass


@singleton
class HydraRuntime(RuntimeVariables):
    pass


class JobReturn:
    def __init__(self):
        self.overrides = None
        self.return_value = None
        self.cfg = None
        self.working_dir = None


def fullname(o):
    if inspect.isclass(o):
        return o.__module__ + "." + o.__qualname__
    else:
        return o.__module__ + "." + o.__class__.__qualname__


def get_method(path):
    return get_class(path)


def get_class(path):
    try:
        from importlib import import_module
        module_path, _, class_name = path.rpartition('.')
        mod = import_module(module_path)
        try:
            klass = getattr(mod, class_name)
        except AttributeError:
            raise ImportError(
                "Class {} is not in module {}".format(
                    class_name, module_path))
        return klass
    except ValueError as e:
        print("Error initializing class " + path)
        raise e


def get_static_method(full_method_name):
    try:
        spl = full_method_name.split('.')
        method_name = spl.pop()
        class_name = '.'.join(spl)
        clz = get_class(class_name)
        return getattr(clz, method_name)
    except Exception as e:
        log.error(
            "Error getting static method {} : {}".format(
                full_method_name, e))
        raise e


def instantiate(config, *args):
    try:
        clazz = get_class(config['class'])
        params = config.params or {}
        return clazz(*args, **params)
    except Exception as e:
        log.error("Error instantiating {} : {}".format(config['class'], e))
        raise e


def create_task(task_class):
    return get_class(task_class)()


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
            '[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    if verbose is not None:
        if verbose == 'root':
            logging.getLogger().setLevel(logging.DEBUG)
        for logger in verbose.split(','):
            logging.getLogger(logger).setLevel(logging.DEBUG)


def save_config(cfg, filename):
    with open(os.path.join(filename), 'w') as file:
        file.write(cfg.pretty())


def get_overrides_dirname(lst):
    lst = copy.deepcopy(lst)
    lst.sort()
    return re.sub(
        pattern='[=]',
        repl=':',
        string=",".join(lst)
    )


def filter_overrides(overrides):
    """
    :param overrides: overrides list
    :return: returning a new overrides list with all the keys starting with hydra. fitlered.
    """
    return [x for x in overrides if not x.startswith('hydra.')]


def run_job(
        config,
        task_function,
        verbose,
        job_dir_key,
        job_subdir_key):
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
        del task_cfg['hydra']
        ret.cfg = task_cfg
        ret.overrides = config.hydra.overrides.task.to_container()
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        os.chdir(working_dir)
        configure_log(config.hydra.task_logging, verbose)
        save_config(task_cfg, 'config.yaml')
        save_config(config.hydra.overrides.task, 'overrides.yaml')
        ret.return_value = task_function(task_cfg)
        return ret
    finally:
        os.chdir(old_cwd)


def setup_globals():
    try:
        # clear resolvers. this is important to flush the resolvers cache
        # (specifically needed for unit tests)
        OmegaConf.clear_resolvers()
        OmegaConf.register_resolver(
            "now", lambda pattern: strftime(
                pattern, localtime()))
        OmegaConf.register_resolver("job", JobRuntime().get)
        OmegaConf.register_resolver("hydra", HydraRuntime().get)

    except AssertionError:
        # calling it again in no_workers mode will throw. safe to ignore.
        pass


def update_job_runtime(cfg):
    JobRuntime().set('name', cfg.hydra.name)
    JobRuntime().set('override_dirname', get_overrides_dirname(cfg.hydra.overrides.task))


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def get_sweep(overrides):
    lists = []
    for s in overrides:
        key, value = s.split('=')
        lists.append(["{}={}".format(key, val)
                      for val in value.split(',')])

    return list(itertools.product(*lists))
