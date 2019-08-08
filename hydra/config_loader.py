"""
Configuration loader
"""

import copy
import os

from omegaconf import OmegaConf, DictConfig, ListConfig
from pkg_resources import resource_stream, resource_exists

from .errors import MissingConfigException


class ConfigLoader:
    """
    Configuration loader
    """

    def __init__(self, conf_dir, conf_filename, strict_task_cfg=False):
        self.cfg_dir = conf_dir
        self.conf_filename = conf_filename
        self.all_config_checked = []
        self.strict_task_cfg = strict_task_cfg

    def get_load_history(self):
        """
        returns the load history (which configs were attempted to load, and if they
        were loaded successfully or not.
        """
        return copy.deepcopy(self.all_config_checked)

    def load_hydra_cfg(self, overrides):
        """
        Loads Hydra configuraiton
        :param overrides: overrides from command line.
        :return:
        """
        hydra_cfg_defaults = self._create_cfg(
            cfg_dir='pkg://hydra.default_conf',
            cfg_filename='hydra.yaml',
            strict=False)
        if os.path.exists(self.cfg_dir) and not os.path.isdir(self.cfg_dir):
            raise IOError(
                "conf_dir is not a directory : {}".format(
                    self.cfg_dir))
        cfg_dir = os.path.join(self.cfg_dir, '.hydra')

        hydra_cfg_path = os.path.join(cfg_dir, "hydra.yaml")
        if os.path.exists(hydra_cfg_path):
            hydra_cfg = self._create_cfg(
                cfg_dir=cfg_dir,
                cfg_filename="hydra.yaml",
                strict=False,
                cli_overrides=overrides)
        else:
            hydra_cfg = OmegaConf.from_dotlist(overrides)
        # strip everything outside of the hydra tree from the hydra config
        hydra_cfg = OmegaConf.merge(hydra_cfg_defaults, hydra_cfg)
        clean = OmegaConf.create()
        clean.hydra = hydra_cfg.hydra
        hydra_cfg = clean
        return hydra_cfg

    def load_task_cfg(self, cli_overrides):
        """
        Loads the task configuration
        :param cli_overrides: config overrides from CLI
        """
        return self._create_cfg(
            cfg_dir=self.cfg_dir,
            cfg_filename=self.conf_filename,
            cli_overrides=cli_overrides,
            strict=self.strict_task_cfg)

    def load_configuration(self, overrides=None):
        """
        Load both the Hydra and the task configuraitons
        :param overrides:
        :return: a dictionary with both configs
        """
        assert overrides is None or isinstance(overrides, list)

        hydra_cfg = self.load_hydra_cfg(overrides or [])

        task_cfg = self._create_cfg(cfg_dir=self.cfg_dir,
                                    cfg_filename=self.conf_filename,
                                    cli_overrides=overrides or [],
                                    strict=self.strict_task_cfg)
        return dict(hydra_cfg=hydra_cfg, task_cfg=task_cfg)

    def _load_config_impl(self, is_pkg, filename):
        loaded_cfg = None
        if is_pkg:
            res_base = os.path.dirname(filename)
            res_file = os.path.basename(filename)
            loaded_cfg = OmegaConf.load(resource_stream(res_base, res_file))
            self.all_config_checked.append(('pkg://' + filename, True))
        elif os.path.exists(filename):
            loaded_cfg = OmegaConf.load(filename)
            self.all_config_checked.append((filename, True))
        else:
            self.all_config_checked.append((filename, False))
        return loaded_cfg

    def _merge_config(self, cfg_dir, is_pkg, cfg, family, name, required):
        if family != '.':
            family_dir = os.path.join(cfg_dir, family)
        else:
            family_dir = cfg_dir
        cfg_path = os.path.join(family_dir, str(name)) + '.yaml'
        new_cfg = self._load_config_impl(is_pkg, cfg_path)
        if new_cfg is None:
            if required:
                if self._exists(is_pkg, family_dir):
                    options = [f[0:-len('.yaml')] for f in os.listdir(family_dir) if
                               os.path.isfile(os.path.join(family_dir, f)) and f.endswith(".yaml")]
                    msg = "Could not load {}, available options:\n{}:\n\t{}".format(
                        cfg_path, family, "\n\t".join(options))
                else:
                    options = None
                    msg = "Could not load {}, directory not found".format(
                        cfg_path, family)
                raise MissingConfigException(msg, cfg_path, options)
            else:
                return cfg
        else:
            return OmegaConf.merge(cfg, new_cfg)

    @staticmethod
    def _exists(is_pkg, filename):
        if is_pkg:
            res_base = os.path.dirname(filename)
            res_file = os.path.basename(filename)
            return resource_exists(res_base, res_file)
        else:
            return os.path.exists(filename)

    def _create_cfg(self, cfg_dir, cfg_filename, strict, cli_overrides=[]):
        is_pkg = cfg_dir.startswith('pkg://')
        if is_pkg:
            cfg_dir = cfg_dir[len('pkg://'):]

        if not is_pkg:
            if not os.path.exists(cfg_dir):
                raise IOError("conf_dir not found : {}".format(cfg_dir))

        if cfg_filename is not None:
            main_cfg_file = os.path.join(cfg_dir, cfg_filename)
            if not ConfigLoader._exists(is_pkg, main_cfg_file):
                raise IOError(
                    "Config file not found : {}".format(
                        os.path.realpath(main_cfg_file)))

            main_cfg = self._load_config_impl(is_pkg, main_cfg_file)
        else:
            main_cfg = OmegaConf.create(dict(defaults=[]))
        if main_cfg.defaults is None:
            main_cfg.defaults = []
        ConfigLoader._validate_config(main_cfg)

        # split overrides into defaults (which cause additional configs to be loaded)
        # and overrides which triggers overriding of specific nodes in the
        # config tree
        overrides = []
        defaults_changes = {}
        for override in copy.deepcopy(cli_overrides):
            key, value = override.split('=')
            assert key != 'optional', "optional is a reserved keyword and cannot be used as a " \
                                      "config group name"
            path = os.path.join(cfg_dir, key)
            if ConfigLoader._exists(is_pkg, path):
                defaults_changes[key] = value
                cli_overrides.remove(override)
            else:
                overrides.append(override)

        ConfigLoader._update_defaults(main_cfg, defaults_changes)

        cfg = main_cfg
        for default in main_cfg.defaults:
            if isinstance(default, DictConfig):
                is_optional = False
                if default.optional is not None:
                    is_optional = default.optional
                    del default['optional']
                family = next(iter(default.keys()))
                name = default[family]
                cfg = self._merge_config(cfg=cfg,
                                         cfg_dir=cfg_dir,
                                         is_pkg=is_pkg,
                                         family=family,
                                         name=name,
                                         required=not is_optional)
            else:
                assert isinstance(default, str)
                cfg = self._merge_config(cfg=cfg,
                                         cfg_dir=cfg_dir,
                                         is_pkg=is_pkg,
                                         family='.',
                                         name=default,
                                         required=True)
        if strict:
            OmegaConf.set_struct(cfg, True)
        # merge in remaining overrides
        cfg.merge_with_dotlist(overrides)
        # remove config block from resulting cfg.
        del cfg['defaults']
        return cfg

    @staticmethod
    def _validate_config(cfg):
        valid_example = """
        Example of a valid defaults:
        defaults:
          - dataset: imagenet
          - model: alexnet
            optional: true
          - optimizer: nesterov
        """
        assert isinstance(
            cfg.defaults,
            ListConfig), "defaults must be a list because composition is order sensitive : " + \
                         valid_example
        for default in cfg.defaults:
            assert isinstance(default, DictConfig) or isinstance(default, str)
            if isinstance(default, DictConfig):
                assert len(default) in (1, 2)
                if len(default) == 2:
                    assert default.optional is not None and isinstance(
                        default.optional, bool)
                else:
                    # optional can't be the only config key in a default
                    assert default.optional is None, "Missing config key"
            elif isinstance(default, str):
                # single file to load
                pass

    @staticmethod
    def _update_defaults(cfg, defaults_changes):
        for default in cfg.defaults:
            if isinstance(default, DictConfig):
                for key in default.keys():
                    if key != 'optional':
                        if key in defaults_changes:
                            default[key] = defaults_changes[key]
                            del defaults_changes[key]
        # unmatched new defaults, put at end of list to be loaded normally
        for key, value in defaults_changes.items():
            cfg.defaults.append({key: value})
