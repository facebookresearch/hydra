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
            path = path.replace("/", ".").replace("\\", ".")
        return is_pkg, path

    def _is_group(self, group_name, search_path):
        for search_path in search_path:
            is_pkg, path = self._split_path(search_path)
            if self._exists(is_pkg, os.path.join(path, group_name)) is True:
                return True
        return False

    def _find_config(self, filepath):
        for search_path in self.full_search_path:
            is_pkg, path = self._split_path(search_path)
            if is_pkg:
                dirname = os.path.dirname(filepath).replace("/", ".").replace("\\", ".")
                basename = os.path.basename(filepath)
                if dirname != "":
                    config_dir = "{}.{}".format(path, dirname)
                else:
                    config_dir = path
                config_file = os.path.join(config_dir, basename)
            else:
                config_file = os.path.join(search_path, filepath)

            config_file = config_file.replace("\\", "/")
            if self._exists(is_pkg, config_file):
                if is_pkg:
                    config_file = "pkg://" + config_file
                return config_file
        return None

    @staticmethod
    def _merge_default_lists(primary, merged_list):
        if isinstance(primary, ListConfig):
            primary = primary.to_container()
        if isinstance(merged_list, ListConfig):
            merged_list = merged_list.to_container()
        key_to_idx = {}
        for idx, d in enumerate(primary):
            if isinstance(d, dict):
                key = next(iter(d.keys()))
                key_to_idx[key] = idx
        result = copy.deepcopy(primary)
        for d in copy.deepcopy(merged_list):
            if isinstance(d, dict):
                key = next(iter(d.keys()))
                if key in key_to_idx.keys():
                    idx = key_to_idx[key]
                    result[idx] = d
                    merged_list.remove(d)
            else:
                result.append(d)
                merged_list.remove(d)

        for d in merged_list:
            result.append(d)

        return result

    @staticmethod
    def _merge_configs(c1, c2):
        merged_defaults = ConfigLoader._merge_default_lists(
            c1.defaults or [], c2.defaults or []
        )
        c3 = OmegaConf.merge(c1, c2)
        c3.defaults = merged_defaults
        return c3

    def _move_hydra_overrides(self, job_overrides, hydra_overrides):
        move_list = []
        for override in job_overrides:
            key, value = override.split("=")
            if self._is_group(key, self.hydra_search_path):
                move_list.append(override)
                job_overrides.remove(override)

        merged = self._merge_default_lists(hydra_overrides, move_list)
        del hydra_overrides[:]
        hydra_overrides.extend(merged)

    def load_configuration(self, overrides=[]):
        assert overrides is None or isinstance(overrides, list)
        overrides = overrides or []

        # Load hydra config
        hydra_cfg = self._load_hydra_cfg(overrides)

        job_overrides = [x for x in overrides if not x.startswith("hydra.")]
        hydra_overrides = [x for x in overrides if x.startswith("hydra.")]

        # Load job config
        job_cfg, consumed_job_defaults = self._create_cfg(
            cfg_filename=self.config_file,
            strict=self.strict_cfg,
            open_defaults=True,
            cli_overrides=job_overrides,
        )

        cfg = self._merge_configs(hydra_cfg, job_cfg)
        cfg = self._merge_defaults(cfg)

        self._move_hydra_overrides(job_overrides, hydra_overrides)

        cfg.hydra.overrides.task.extend(job_overrides)
        cfg.hydra.overrides.hydra.extend(hydra_overrides)

        job = OmegaConf.create(dict(name=JobRuntime().get("name")))
        cfg.hydra.job = OmegaConf.merge(job, cfg.hydra.job)
        OmegaConf.set_struct(cfg, self.strict_cfg)

        # Merge all command line overrides after enabling strict flag
        value_overrides = []
        for jo in job_overrides + hydra_overrides:
            if jo not in consumed_job_defaults:
                value_overrides.append(jo)
        cfg.merge_with_dotlist(value_overrides)
        return cfg

    def load_sweep_config(self, master_config, sweep_overrides):
        # Recreate the config for this sweep instance with the appropriate overrides
        sweep_config = self.load_configuration(
            master_config.hydra.overrides.hydra.to_container() + sweep_overrides
        )

        # Copy old config cache to ensure we get the same resolved values (for things like timestamps etc)
        OmegaConf.copy_cache(from_config=master_config, to_config=sweep_config)

        return sweep_config

    def _load_hydra_cfg(self, overrides):
        """
        Loads Hydra configuration
        :param overrides: overrides from command line.
        :return:
        """
        hydra_cfg_defaults, _ = self._create_cfg(
            cfg_filename="default_hydra.yaml", strict=False
        )
        hydra_cfg, consumed_defaults = self._create_cfg(
            cfg_filename="hydra.yaml",
            strict=False,
            cli_overrides=overrides,
            open_defaults=False,
        )
        hydra_cfg = self._merge_configs(hydra_cfg_defaults, hydra_cfg)
        for consumed in consumed_defaults:
            hydra_cfg.hydra.overrides.hydra.append(consumed)
            overrides.remove(consumed)

        return hydra_cfg

    def _load_config_impl(self, input_file):
        loaded_cfg = None
        filename = self._find_config(input_file)
        if filename is None:
            self.all_config_checked.append((input_file.replace("\\", "/"), False))
        else:
            is_pkg = filename.startswith("pkg://")
            if is_pkg:
                filename = filename[len("pkg://") :]
                res_path = os.path.dirname(filename)
                res_file = os.path.basename(filename)
                with resource_stream(res_path, res_file) as stream:
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
                if self.exists(search_path) and resource_isdir(path, group_name):
                    files = resource_listdir(path, group_name)
            else:
                group_path = os.path.join(path, group_name)
                if os.path.isdir(group_path):
                    files = os.listdir(group_path)
            files = [f for f in files if f.endswith(".yaml")]
            files = [f[0 : -len(".yaml")] for f in files]
            options.extend(files)
        return options

    def _merge_config(self, cfg, family, name, required):

        if family != ".":
            new_cfg = os.path.join(family, name)
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

    def exists_in_search_path(self, filepath):
        return self._find_config(filepath) is not None

    def exists(self, filename):
        is_pkg, path = self._split_path(filename)
        return ConfigLoader._exists(is_pkg, path)

    @staticmethod
    def _exists(is_pkg, filename):
        if is_pkg:
            res_base = os.path.dirname(filename)
            res_file = os.path.basename(filename)
            if res_base == "":
                res_base = res_file
                res_file = ""
            try:
                return resource_exists(res_base, res_file)
            except ImportError:
                return False
            except ValueError:  # Python 2.7 throws ValueError empty module name sometimes.
                return False
        else:
            return os.path.exists(filename)

    def _merge_defaults(self, cfg):
        cfg_defaults = cfg.defaults.to_container()
        for default in cfg.defaults:
            default_copy = copy.deepcopy(default)
            if isinstance(default, DictConfig):
                is_optional = False
                if default.optional is not None:
                    is_optional = default.optional
                    del default["optional"]
                family = next(iter(default.keys()))
                name = default[family]
                # Name is none if default value is removed
                if name is not None:
                    cfg = self._merge_config(
                        cfg=cfg,
                        family=family,
                        name="{}.yaml".format(name),
                        required=not is_optional,
                    )
                cfg_defaults.remove(default_copy)
            else:
                assert isinstance(default, str)
                cfg = self._merge_config(
                    cfg=cfg, family="", name="{}.yaml".format(default), required=True
                )
                cfg_defaults.remove(default)
        cfg.defaults = cfg_defaults
        # remove config block from resulting cfg.
        if len(cfg.defaults) == 0:
            del cfg["defaults"]
        return cfg

    def _create_cfg(self, cfg_filename, strict, cli_overrides=[], open_defaults=True):
        """
        :param cfg_filename:
        :param strict:
        :param cli_overrides:
        :param open_defaults: Allow adding loading additional keys to defaults.
        :return:
        """
        resolved_cfg_filename = (
            self._find_config(cfg_filename) if cfg_filename is not None else None
        )
        if resolved_cfg_filename is None:
            main_cfg = OmegaConf.create()
        else:
            main_cfg = self._load_config_impl(cfg_filename)
            if main_cfg is None:
                raise IOError(
                    "could not find {}, config path:\n\t".format(
                        cfg_filename, "\n\t".join(self.full_search_path)
                    )
                )
        assert main_cfg is not None

        if main_cfg.defaults is None:
            main_cfg.defaults = []
        ConfigLoader._validate_config(main_cfg)

        # split overrides into defaults (which cause additional configs to be loaded)
        # and overrides which triggers overriding of specific nodes in the
        # config tree
        overrides = []
        defaults_changes = {}
        consumed_defaults = []
        for override in copy.deepcopy(cli_overrides):
            key, value = override.split("=")
            assert key != "optional", (
                "optional is a reserved keyword and cannot be used as a "
                "config group name"
            )

            can_add = open_defaults
            for d in main_cfg.defaults:
                if isinstance(d, DictConfig) and key in d:
                    can_add = True
                    break
            # Do not add sweep configs into defaults, those will be added to the sweep config
            # after the list is broken into items
            if "," in value:
                can_add = False
            if can_add and self._is_group(key, self.full_search_path):
                defaults_changes[key] = value
                consumed_defaults.append(override)
            else:
                overrides.append(override)

        self._update_defaults(main_cfg, defaults_changes)
        if strict:
            OmegaConf.set_struct(main_cfg, True)

        return main_cfg, consumed_defaults

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
        assert isinstance(cfg.defaults, ListConfig), (
            "defaults must be a list because composition is order sensitive : "
            + valid_example
        )
        for default in cfg.defaults:
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
