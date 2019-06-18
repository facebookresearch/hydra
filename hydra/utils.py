import inspect
import logging
import logging.config
import os

from time import strftime, localtime

from omegaconf import OmegaConf
from hydra.task import Task

log = logging.getLogger(__name__)


def fullname(o):
    if inspect.isclass(o):
        return o.__module__ + "." + o.__qualname__
    else:
        return o.__module__ + "." + o.__class__.__qualname__


def get_class(path):
    try:
        from importlib import import_module
        module_path, _, class_name = path.rpartition('.')
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
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
        log.error("Error getting static method {} : {}".format(full_method_name, e))
        raise e


def instantiate(config, *args):
    try:
        clazz = get_class(config['class'])
        return clazz(*args, **(config.params or {}))
    except Exception as e:
        log.error("Error instantiating {config.clazz} : {e}")
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


def validate_hydra_cfg(hydra_cfg):
    order = hydra_cfg.load_order or []
    for key in (hydra_cfg.configs or {}):
        if key not in order:
            raise RuntimeError("'{}' load order is not specified in load_order".format(key))


def create_task_cfg(cfg_dir, task, cli_overrides=[]):
    loaded_configs = []
    all_config_checked = []

    def load_config(filename):
        loaded_cfg = None
        if os.path.exists(filename):
            loaded_cfg = OmegaConf.load(filename)
            loaded_configs.append(filename)
            all_config_checked.append((filename, True))
        else:
            all_config_checked.append((filename, False))
        return loaded_cfg

    def merge_config(cfg_, family_, name_, required):
        family_dir = os.path.join(cfg_dir, family_)
        cfg_path = os.path.join(family_dir, name_) + '.yaml'
        new_cfg = load_config(cfg_path)
        if new_cfg is None:
            if required:
                options = [f[0:-len('.yaml')] for f in os.listdir(family_dir) if
                           os.path.isfile(os.path.join(family_dir, f)) and f.endswith(".yaml")]
                raise IOError("Could not load {}, available options : {}".format(cfg_path, ",".join(options)))
            else:
                return cfg_
        else:
            return OmegaConf.merge(cfg_, new_cfg)

    task_name = task.split('.')[-1]
    hydra_cfg_path = os.path.join(cfg_dir, "hydra.yaml")
    hydra_cfg = OmegaConf.load(hydra_cfg_path)

    # split overrides into defaults (which cause additional configs to be loaded)
    # and overrides which triggers overriding of specific nodes in the config tree
    overrides = []
    for override in cli_overrides:
        key, value = override.split('=')
        path = os.path.join(cfg_dir, key)
        if os.path.exists(path):
            hydra_cfg.configs[key] = value
        else:
            overrides.append(override)

    validate_hydra_cfg(hydra_cfg)

    main_conf = os.path.join(cfg_dir, "{}.yaml".format(task_name))
    cfg = load_config(main_conf)
    if cfg is None:
        raise IOError("Could not load {}".format(main_conf))
    for family in hydra_cfg.load_order:
        name = hydra_cfg.configs[family]
        is_optional = family in (hydra_cfg.optional or [])
        cfg = merge_config(cfg, family, name, required=not is_optional)

    cfg = OmegaConf.merge(cfg, OmegaConf.from_cli(overrides))
    return dict(hydra_cfg=hydra_cfg, cfg=cfg, loaded=loaded_configs, checked=all_config_checked)


def configure_log(cfg_dir, cfg, verbose=None):
    # configure target directory for all logs files (binary, text. models etc)
    log_config = cfg.log_config
    if not os.path.isabs(log_config):
        log_config = os.path.join(cfg_dir, log_config)

    logging.config.dictConfig(OmegaConf.load(log_config).to_dict())

    if verbose:
        if verbose == 'root':
            logging.getLogger().setLevel(logging.DEBUG)
        for logger in verbose.split(','):
            logging.getLogger(logger).setLevel(logging.DEBUG)


def save_config(cfg, filename):
    with open(os.path.join(filename), 'w') as file:
        file.write(cfg.pretty())


def run_job(task, overrides, verbose, working_directory):
    cfg_dir = find_cfg_dir(task)
    task_cfg = create_task_cfg(cfg_dir, task, overrides)
    cfg = task_cfg['cfg']
    hydra_cfg = task_cfg['hydra_cfg']
    old_cwd = os.getcwd()
    try:
        job_wd = hydra_cfg.working_directory[working_directory]
        assert job_wd is not None
        os.makedirs(job_wd)
        os.chdir(job_wd)
        configure_log(cfg_dir, hydra_cfg, verbose)
        task = create_task(task)
        assert isinstance(task, Task)
        save_config(cfg, 'config.yaml')
        task.setup(cfg)
        task.run(cfg)
    finally:
        os.chdir(old_cwd)
