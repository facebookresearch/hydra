from pkg_resources import resource_stream, resource_exists
import inspect
import logging
import logging.config
import os
import re
import sys
from time import strftime, localtime

from omegaconf import OmegaConf, ListConfig, DictConfig

from hydra.errors import MissingConfigException

log = logging.getLogger(__name__)


def singleton(class_):
    instances = {}

    def instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return instance


@singleton
class JobRuntime:
    def __init__(self):
        self.conf = OmegaConf.create()

    def get(self, key):
        ret = self.conf.select(key)
        if ret is None:
            raise KeyError("Key not found in JobRuntime: {}".format(key))
        return ret

    def set(self, key, value):
        log.info("Setting job:{}={}".format(key, value))
        self.conf[key] = value


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


def validate_config(cfg):
    if cfg.defaults is None:
        return
    valid_example = """
    Example of a valid defaults:
    defaults:
      - dataset: imagenet
      - model: alexnet
        optional: true
      - optimizer: nesterov
    """
    assert isinstance(cfg.defaults,
                      ListConfig), "defaults must be a list because composition is order sensitive : " + valid_example
    for default in cfg.defaults:
        assert isinstance(default, DictConfig), "elements of defaults list must be dictionaries"
        assert len(default) in (1, 2)
        if len(default) == 2:
            assert default.optional is not None and type(default.optional) == bool
        else:
            # optional can't be the only config key in a default
            assert default.optional is None, "Missing config key"


def update_defaults(cfg, defaults_changes):
    for default in cfg.defaults:
        for key in default.keys():
            if key != 'optional':
                if key in defaults_changes:
                    default[key] = defaults_changes[key]
                    del defaults_changes[key]
    # unmatched new defaults, put at end of list
    for key, value in defaults_changes.items():
        cfg.defaults.append({key: value})


def create_hydra_cfg(cfg_dir, hydra_cfg_defaults, overrides):
    cfg_dir = os.path.join(cfg_dir, '.hydra')
    if os.path.exists(cfg_dir) and not os.path.isdir(cfg_dir):
        raise IOError("conf_dir is not a directory : {}".format(cfg_dir))

    if hydra_cfg_defaults is None:
        hydra_cfg_defaults = OmegaConf.create()

    hydra_cfg_path = os.path.join(cfg_dir, "hydra.yaml")
    if os.path.exists(hydra_cfg_path):
        hydra_cfg_out = create_cfg(cfg_dir, "hydra.yaml", overrides)
        hydra_cfg = hydra_cfg_out['cfg']
        # TODO: potentially allow debugging hydra config construction
    else:
        hydra_cfg = OmegaConf.create()

    hydra_cfg = OmegaConf.merge(hydra_cfg_defaults, hydra_cfg)
    clean = OmegaConf.create()
    clean.hydra = hydra_cfg.hydra
    hydra_cfg = clean

    hydra_overrides = [x for x in overrides if x.startswith("hydra.")]
    # remove all matching overrides from overrides list
    for override in hydra_overrides:
        overrides.remove(override)
    return hydra_cfg


def create_cfg(cfg_dir, cfg_filename, cli_overrides=[], defaults_only=False):
    is_pkg = cfg_dir.startswith('pkg://')
    if is_pkg:
        cfg_dir = cfg_dir[len('pkg://'):]
    loaded_configs = []
    all_config_checked = []

    if not is_pkg:
        if not os.path.exists(cfg_dir):
            raise IOError("conf_dir not found : {}".format(cfg_dir))

    def load_config(filename):
        loaded_cfg = None
        if is_pkg:
            res_base = os.path.dirname(filename)
            res_file = os.path.basename(filename)
            loaded_cfg = OmegaConf.load(resource_stream(res_base, res_file))
        elif os.path.exists(filename):
            loaded_cfg = OmegaConf.load(filename)
            loaded_configs.append(filename)
            all_config_checked.append((filename, True))
        else:
            all_config_checked.append((filename, False))
        return loaded_cfg

    def merge_config(cfg_, family_, name_, required):
        if family_ != '.':
            family_dir = os.path.join(cfg_dir, family_)
        else:
            family_dir = cfg_dir
        cfg_path = os.path.join(family_dir, name_) + '.yaml'
        new_cfg = load_config(cfg_path)
        if new_cfg is None:
            if required:
                options = [f[0:-len('.yaml')] for f in os.listdir(family_dir) if
                           os.path.isfile(os.path.join(family_dir, f)) and f.endswith(".yaml")]
                msg = "Could not load {}, available options:\n{}:\n\t{}".format(cfg_path, family_, "\n\t".join(options))
                raise MissingConfigException(msg, cfg_path, options)
            else:
                return cfg_
        else:
            return OmegaConf.merge(cfg_, new_cfg)

    def exists(filename):
        if is_pkg:
            res_base = os.path.dirname(filename)
            res_file = os.path.basename(filename)
            return resource_exists(res_base, res_file)
        else:
            return os.path.exists(filename)

    if cfg_filename is not None:
        main_cfg_file = os.path.join(cfg_dir, cfg_filename)
        if not exists(main_cfg_file):
            raise IOError("Config file not found : {}".format(os.path.realpath(main_cfg_file)))

        main_cfg = load_config(main_cfg_file)
    else:
        main_cfg = OmegaConf.create(dict(defaults=[]))
    if main_cfg.defaults is None:
        main_cfg.defaults = []
    validate_config(main_cfg)

    # split overrides into defaults (which cause additional configs to be loaded)
    # and overrides which triggers overriding of specific nodes in the config tree
    overrides = []
    defaults_changes = {}
    for override in cli_overrides:
        key, value = override.split('=')
        assert key != 'optional', "optional is a reserved keyword and cannot be used as a config group name"
        path = os.path.join(cfg_dir, key)
        if exists(path):
            defaults_changes[key] = value
        else:
            overrides.append(override)

    update_defaults(main_cfg, defaults_changes)

    cfg = main_cfg
    for default in main_cfg.defaults:
        is_optional = False
        if default.optional is not None:
            is_optional = default.optional
            del default['optional']
        family, name = next(iter(default.items()))
        cfg = merge_config(cfg, family, name, required=not is_optional)

    if not defaults_only:
        # merge in remaining overrides
        cfg = OmegaConf.merge(cfg, OmegaConf.from_cli(overrides))
    # remove config block from resulting cfg.
    del cfg['defaults']
    return dict(cfg=cfg, loaded=loaded_configs, checked=all_config_checked)


def configure_log(log_config, verbose=None):
    if log_config is not None:
        conf = log_config.to_container(resolve=True)
        logging.config.dictConfig(conf)
    else:
        # default logging to stdout
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
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


def run_job(cfg_dir, cfg_filename, hydra_cfg, task_function, overrides, verbose, job_dir, job_subdir_key):
    task_cfg = create_cfg(cfg_dir=cfg_dir, cfg_filename=cfg_filename, cli_overrides=overrides)
    cfg = task_cfg['cfg']

    old_cwd = os.getcwd()
    working_dir = job_dir
    if job_subdir_key is not None:
        # evaluate job_subdir_key lazily.
        # this is running on the client side in sweep and contains things such as job:id which
        # are only available there.
        subdir = hydra_cfg.select(job_subdir_key)
        working_dir = os.path.join(working_dir, subdir)

    try:
        ret = JobReturn()
        ret.working_dir = working_dir
        ret.cfg = cfg
        ret.overrides = overrides
        os.makedirs(working_dir, exist_ok=True)
        os.chdir(working_dir)
        configure_log(hydra_cfg.hydra.logging, verbose)
        save_config(cfg, 'config.yaml')
        ret.return_value = task_function(cfg)
        return ret
    finally:
        os.chdir(old_cwd)


def setup_globals():
    try:
        OmegaConf.register_resolver("now", lambda pattern: strftime(pattern, localtime()))
        OmegaConf.register_resolver("job", JobRuntime().get)
    except AssertionError:
        # calling it again in no_workers mode will throw. safe to ignore.
        pass


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
