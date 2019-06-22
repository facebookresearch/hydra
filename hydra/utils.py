import inspect
import logging
import logging.config
import os
import sys

from omegaconf import OmegaConf
from time import strftime, localtime

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


def validate_config(cfg):
    valid_example = """
    Example of a valid defaults:
    defaults:
      - dataset: imagenet
      - model: alexnet
        optional: true
      - optimizer: nesterov
    """
    assert cfg.defaults.is_sequence(), \
        "defaults must be a list because composition is order sensitive : " + valid_example
    for default in cfg.defaults:
        assert default.is_dict()
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


def create_hydra_cfg(target_file, cfg_dir, overrides):
    hydra_cfg_path = os.path.join(cfg_dir, "hydra.yaml")
    if os.path.exists(hydra_cfg_path):
        hydra_cfg = OmegaConf.load(hydra_cfg_path)
    else:
        hydra_cfg = OmegaConf.create(dict(
            hydra=dict(
                run_dir='./outputs/${now:%Y-%m-%d_%H-%M-%S}',
                sweep_dir='???'
            ))
        )
    hydra_overrides = [x for x in overrides if x.startswith("hydra.")]
    # remove all matching overrides from overrides list
    for override in hydra_overrides:
        overrides.remove(override)
    hydra_cfg.merge_with_dotlist(hydra_overrides)
    target_file = os.path.basename(target_file)
    hydra_cfg.hydra.name = os.path.splitext(target_file)[0]  # TODO: this should only replace name if it's '???'
    return hydra_cfg


def create_task_cfg(cfg_dir, cfg_filename, cli_overrides=[]):
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

    main_cfg_file = os.path.join(cfg_dir, cfg_filename)
    if os.path.exists(main_cfg_file):
        main_cfg = load_config(main_cfg_file)
    else:
        main_cfg = OmegaConf.create(dict(defaults={}))
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
        if os.path.exists(path):
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

    cfg = OmegaConf.merge(cfg, OmegaConf.from_cli(overrides))
    # remove config block from resulting cfg.
    del cfg['defaults']
    return dict(cfg=cfg, loaded=loaded_configs, checked=all_config_checked)


def configure_log(log_config, verbose=None):
    if log_config is not None:
        logging.config.dictConfig(log_config.to_dict())
    else:
        # default logging to stdout
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    if verbose:
        if verbose == 'root':
            logging.getLogger().setLevel(logging.DEBUG)
        for logger in verbose.split(','):
            logging.getLogger(logger).setLevel(logging.DEBUG)


def save_config(cfg, filename):
    with open(os.path.join(filename), 'w') as file:
        file.write(cfg.pretty())


def run_job(cfg_dir, cfg_filename, hydra_cfg, task_function, overrides, verbose, workdir):
    task_cfg = create_task_cfg(cfg_dir=cfg_dir, cfg_filename=cfg_filename, cli_overrides=overrides)
    cfg = task_cfg['cfg']
    if cfg.sweep_id is not None:
        hydra_cfg.sweep_id = cfg.sweep_id
    old_cwd = os.getcwd()
    hydra_cfg.hydra.job_cwd = workdir
    try:
        os.makedirs(workdir)
        os.chdir(workdir)
        configure_log(hydra_cfg.hydra.logging, verbose)
        save_config(cfg, 'config.yaml')
        task_function(cfg)
    finally:
        os.chdir(old_cwd)


def setup_globals():
    OmegaConf.register_resolver("now", lambda pattern: strftime(pattern, localtime()))
