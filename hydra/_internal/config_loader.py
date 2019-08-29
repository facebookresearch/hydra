# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""

import copy
import os

from omegaconf import OmegaConf, DictConfig, ListConfig
from pkg_resources import (
    resource_stream,
    resource_exists,
    resource_listdir,
    resource_isdir,
)

from ..errors import MissingConfigException
from ..plugins.common.utils import JobRuntime


class ConfigLoader:
    """
    Configuration loader
    """

    def __init__(
        self, config_file, strict_cfg, hydra_search_path=[], job_search_path=[]
    ):
        self.config_file = config_file
        self.job_search_path = job_search_path
        self.hydra_search_path = hydra_search_path
        self.full_search_path = self.job_search_path + self.hydra_search_path
        self.all_config_checked = []
        self.strict_cfg = strict_cfg

    def load_configuration(self, overrides=[]):
        assert overrides is None or isinstance(overrides, list)
        overrides = overrides or []

        # Load hydra config
        hydra_cfg = self._create_cfg(cfg_filename="hydra.yaml")

        # Load job config
        job_cfg = self._create_cfg(cfg_filename=self.config_file)

        cfg = self._merge_configs(hydra_cfg, job_cfg)
        consumed_hydra_defaults = self._apply_defaults_overrides(
            cfg, overrides, "all_defaults.hydra"
        )
        consumed_job_defaults = self._apply_defaults_overrides(
            cfg, overrides, "all_defaults.job"
        )
        consumed_free_job_defaults = self._apply_free_defaults(cfg, overrides)
        self._validate_config(cfg)
        cfg = self._merge_defaults(cfg)

        job = OmegaConf.create(dict(name=JobRuntime().get("name")))
        cfg.hydra.job = OmegaConf.merge(job, cfg.hydra.job)

        OmegaConf.set_struct(cfg, self.strict_cfg)

        # Merge all command line overrides after enabling strict flag
        all_consumed = consumed_hydra_defaults + consumed_free_job_defaults
        remaining_overrides = [x for x in overrides if x not in all_consumed]
        cfg.merge_with_dotlist(remaining_overrides)

        remaining = (
            consumed_hydra_defaults
            + consumed_job_defaults
            + consumed_free_job_defaults
            + remaining_overrides
        )

        def is_hydra(x):
            return x.startswith("hydra.") or x.startswith("hydra/")

        job_overrides = [x for x in remaining if not is_hydra(x)]
        hydra_overrides = [x for x in remaining if is_hydra(x)]
        cfg.hydra.overrides.task.extend(job_overrides)
        cfg.hydra.overrides.hydra.extend(hydra_overrides)

        return cfg

    def load_sweep_config(self, master_config, sweep_overrides):
        # Recreate the config for this sweep instance with the appropriate overrides
        overrides = master_config.hydra.overrides.hydra.to_container() + sweep_overrides
        sweep_config = self.load_configuration(overrides)

        # Copy old config cache to ensure we get the same resolved values (for things like timestamps etc)
        OmegaConf.copy_cache(from_config=master_config, to_config=sweep_config)

        return sweep_config

    def exists_in_search_path(self, filepath):
        return self._find_config(filepath) is not None

    def exists(self, filename):
        is_pkg, path = self._split_path(filename)
        return ConfigLoader._exists(is_pkg, path)

    def get_job_search_path(self):
        return self.job_search_path

    def get_hydra_search_path(self):
        return self.hydra_search_path

    def get_load_history(self):
        """
        returns the load history (which configs were attempted to load, and if they
        were loaded successfully or not.
        """
        return copy.deepcopy(self.all_config_checked)

    @staticmethod
    def _split_path(path):
        prefix = "pkg://"
        is_pkg = path.startswith(prefix)
        if is_pkg:
            path = path[len(prefix) :]
        return is_pkg, path

    def _is_group(self, group_name, search_path):
        for search_path in search_path:
            is_pkg, path = self._split_path(search_path)
            if self._exists(is_pkg, "{}/{}".format(path, group_name)) is True:
                return True
        return False

    def _find_config(self, filepath):
        for search_path in self.full_search_path:
            is_pkg, path = self._split_path(search_path)
            config_file = "{}/{}".format(path, filepath)
            if self._exists(is_pkg, config_file):
                if is_pkg:
                    config_file = "pkg://" + config_file
                return config_file
        return None

    @staticmethod
    def _apply_defaults_overrides(cfg, overrides, defaults_key):
        consumed = []
        key_to_idx = {}
        defaults = cfg.select(defaults_key)
        for idx, d in enumerate(defaults):
            if isinstance(d, DictConfig):
                key = next(iter(d.keys()))
                key_to_idx[key] = idx
        for override in copy.deepcopy(overrides):
            key, value = override.split("=")
            if key in key_to_idx:
                # Do not add sweep configs into defaults, those will be added to the sweep config
                # after the list is broken into items
                if "," not in value:
                    if value == "null":
                        del defaults[key_to_idx[key]]
                    else:
                        defaults[key_to_idx[key]][key] = value
                    overrides.remove(override)
                    consumed.append(override)
        return consumed

    def _apply_free_defaults(self, cfg, overrides):
        consumed = []
        for override in overrides:
            key, value = override.split("=")
            if self.exists_in_search_path(key):
                # Do not add sweep configs into defaults, those will be added to the defaults
                # during sweep when after list is broken into items
                if "," not in value:
                    cfg.all_defaults.job.append({key: value})
                    consumed.append(override)

        return consumed

    @staticmethod
    def _merge_default_lists(primary, merged_list):
        def get_key(d1):
            keys_iter = iter(d1.keys())
            key1 = next(keys_iter)
            if key1 == "optional":
                key1 = next(keys_iter)
            return key1

        key_to_idx = {}
        for idx, d in enumerate(primary):
            if isinstance(d, (dict, DictConfig)):
                key = get_key(d)
                key_to_idx[key] = idx
        for d in merged_list:
            if isinstance(d, (dict, DictConfig)):
                key = get_key(d)
                if key in key_to_idx.keys():
                    idx = key_to_idx[key]
                    primary[idx] = d
                    merged_list.remove(d)
            else:
                primary.append(d)
                merged_list.remove(d)

        for d in merged_list:
            primary.append(d)

    @staticmethod
    def _merge_configs(hydra_cfg, job_cfg):
        cfg = OmegaConf.merge(hydra_cfg, job_cfg)
        cfg.all_defaults = dict(
            hydra=hydra_cfg.defaults or [], job=job_cfg.defaults or []
        )
        del cfg["defaults"]
        # Use hydra/ overrides from job defaults to override hydra.defaults
        merge_to_hydra = []
        for default in cfg.all_defaults.job:
            if isinstance(default, DictConfig):
                keys_iter = iter(default.keys())
                key = next(keys_iter)
                if key == "optional":
                    key = next(keys_iter)
                if key.startswith("hydra/"):
                    merge_to_hydra.append(default)
                    cfg.all_defaults.job.remove(default)
        ConfigLoader._merge_default_lists(cfg.all_defaults.hydra, merge_to_hydra)
        return cfg

    def _load_config_impl(self, input_file):
        loaded_cfg = None
        filename = self._find_config(input_file)
        if filename is None:
            self.all_config_checked.append((input_file.replace("\\", "/"), False))
        else:
            is_pkg = filename.startswith("pkg://")
            if is_pkg:
                filename = filename[len("pkg://") :]
                module_name, resource_name = ConfigLoader._split_module_and_resource(
                    filename
                )
                with resource_stream(module_name, resource_name) as stream:
                    loaded_cfg = OmegaConf.load(stream)
                self.all_config_checked.append(("pkg://" + filename, True))
            elif os.path.exists(filename):
                loaded_cfg = OmegaConf.load(filename)
                self.all_config_checked.append((filename, True))
            else:
                assert False
        return loaded_cfg

    def _get_group_options(self, group_name):
        options = []
        for search_path in self.full_search_path:
            is_pkg, path = self._split_path(search_path)
            files = []
            if is_pkg:
                module_name, resource_name = ConfigLoader._split_module_and_resource(
                    "{}/{}".format(path, group_name)
                )
                if self._exists(is_pkg, path) and resource_isdir(
                    module_name, resource_name
                ):
                    files = resource_listdir(module_name, resource_name)
            else:
                group_path = "{}/{}".format(path, group_name)
                if os.path.isdir(group_path):
                    files = os.listdir(group_path)
            files = [f for f in files if f.endswith(".yaml")]
            files = [f[0 : -len(".yaml")] for f in files]
            options.extend(files)
        return options

    def _merge_config(self, cfg, family, name, required):

        if family != ".":
            new_cfg = "{}/{}".format(family, name)
        else:
            new_cfg = name

        loaded_cfg = self._load_config_impl(new_cfg)
        if loaded_cfg is None:
            if required:
                if family == "":
                    msg = "Could not load {}".format(new_cfg)
                    raise MissingConfigException(msg, new_cfg)
                else:
                    options = self._get_group_options(family)
                    if options:
                        msg = "Could not load {}, available options:\n{}:\n\t{}".format(
                            new_cfg, family, "\n\t".join(options)
                        )
                    else:
                        msg = "Could not load {}".format(new_cfg)
                    raise MissingConfigException(msg, new_cfg, options)
            else:
                return cfg

        else:
            return OmegaConf.merge(cfg, loaded_cfg)

        assert False

    @staticmethod
    def _split_module_and_resource(filename):
        sep = filename.find("/")
        if sep == -1:
            module_name = filename
            resource_name = ""
        else:
            module_name = filename[0:sep]
            resource_name = filename[sep + 1 :]
        if module_name == "":
            # if we have a module a module only, dirname would return nothing and basename would return the module.
            module_name = resource_name
            resource_name = ""

        return module_name, resource_name

    @staticmethod
    def _exists(is_pkg, filename):
        if is_pkg:
            module_name, resource_name = ConfigLoader._split_module_and_resource(
                filename
            )
            try:
                return resource_exists(module_name, resource_name)
            except ImportError:
                return False
            except ValueError:  # Python 2.7 throws ValueError empty module name sometimes.
                return False
            except NotImplementedError:
                raise NotImplementedError(
                    "Unable to load {}/{}, are you missing an __init__.py?".format(
                        module_name, resource_name
                    )
                )
        else:
            return os.path.exists(filename)

    def _merge_defaults(self, cfg):
        def merge_defaults(cfg2, defaults_to_merge):
            cfg2.defaults = defaults_to_merge
            for default in cfg2.defaults:
                if isinstance(default, DictConfig):
                    is_optional = False
                    if default.optional is not None:
                        is_optional = default.optional
                        del default["optional"]
                    family = next(iter(default.keys()))
                    name = default[family]
                    # Name is none if default value is removed
                    if name is not None:
                        cfg2 = self._merge_config(
                            cfg=cfg2,
                            family=family,
                            name="{}.yaml".format(name),
                            required=not is_optional,
                        )
                else:
                    assert isinstance(default, str)
                    cfg2 = self._merge_config(
                        cfg=cfg2,
                        family="",
                        name="{}.yaml".format(default),
                        required=True,
                    )
            return cfg2

        for _, defaults in cfg.all_defaults.items():
            cfg = merge_defaults(cfg, defaults)
        del cfg["all_defaults"]
        del cfg["defaults"]
        return cfg

    def _create_cfg(self, cfg_filename):
        if cfg_filename is None:
            cfg = OmegaConf.create()
        else:
            cfg = self._load_config_impl(cfg_filename)
            if cfg is None:
                raise IOError(
                    "could not find {}, config path:\n\t".format(
                        cfg_filename, "\n\t".join(self.full_search_path)
                    )
                )
        if cfg.defaults is not None:
            self._validate_defaults(cfg.defaults)
        return cfg

    @staticmethod
    def _validate_defaults(defaults):
        valid_example = """
        Example of a valid defaults:
        defaults:
          - dataset: imagenet
          - model: alexnet
            optional: true
          - optimizer: nesterov
        """
        if not isinstance(defaults, ListConfig):
            raise ValueError(
                "defaults must be a list because composition is order sensitive, "
                + valid_example
            )

        for default in defaults:
            assert isinstance(default, DictConfig) or isinstance(default, str)
            if isinstance(default, DictConfig):
                assert len(default) in (1, 2)
                if len(default) == 2:
                    assert default.optional is not None and isinstance(
                        default.optional, bool
                    )
                else:
                    # optional can't be the only config key in a default
                    assert default.optional is None, "Missing config key"
            elif isinstance(default, str):
                # single file to load
                pass

    @staticmethod
    def _validate_config(cfg):

        assert isinstance(cfg.all_defaults, DictConfig)
        for _, defaults in cfg.all_defaults.items():
            ConfigLoader._validate_defaults(defaults)

    @staticmethod
    def _update_defaults(cfg, defaults_changes):
        for default in cfg.defaults or []:
            if isinstance(default, DictConfig):
                for key in default.keys():
                    if key != "optional":
                        if key in defaults_changes:
                            default[key] = defaults_changes[key]
                            del defaults_changes[key]
        # unmatched new defaults, put at end of list to be loaded normally
        for key, value in defaults_changes.items():
            cfg.defaults.append({key: value})
