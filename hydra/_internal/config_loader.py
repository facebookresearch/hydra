# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""

import copy
import os

from omegaconf import OmegaConf, DictConfig, ListConfig, open_dict
from pkg_resources import (
    resource_stream,
    resource_exists,
    resource_listdir,
    resource_isdir,
)

from .config_search_path import ConfigSearchPath
from ..errors import MissingConfigException
from ..plugins.common.utils import JobRuntime, get_overrides_dirname, split_key_val


class ConfigLoader:
    """
    Configuration loader
    """

    def __init__(self, config_search_path, default_strict=None):
        assert isinstance(config_search_path, ConfigSearchPath)
        self.config_search_path = config_search_path
        self.default_strict = default_strict
        self.all_config_checked = []

    def load_configuration(self, config_file, overrides=[], strict=None):
        assert config_file is None or isinstance(config_file, str)
        assert strict is None or isinstance(strict, bool)
        assert isinstance(overrides, list)
        if strict is None:
            strict = self.default_strict

        assert overrides is None or isinstance(overrides, list)
        overrides = copy.deepcopy(overrides) or []

        if config_file is not None and not self.exists_in_search_path(config_file):
            raise MissingConfigException(
                missing_cfg_file=config_file,
                message="Cannot find primary config file: {}\nSearch path:\n{}".format(
                    config_file,
                    "\n".join(
                        [
                            "\t{} (from {})".format(x.path, x.provider)
                            for x in self.config_search_path.config_search_path
                        ]
                    ),
                ),
            )

        # Load hydra config
        hydra_cfg = self._create_cfg(cfg_filename="hydra.yaml")

        # Load job config
        job_cfg = self._create_cfg(cfg_filename=config_file, record_load=False)

        defaults = hydra_cfg.defaults or []
        if config_file is not None:
            defaults.append(config_file)
        split_at = len(defaults)
        ConfigLoader._merge_default_lists(defaults, job_cfg.defaults or [])
        consumed = self._apply_defaults_overrides(overrides, defaults)

        consumed_free_job_defaults = self._apply_free_defaults(defaults, overrides)

        ConfigLoader._validate_defaults(defaults)

        # Load and defaults and merge them into cfg
        cfg = self._merge_defaults(hydra_cfg, defaults, split_at)
        OmegaConf.set_struct(cfg.hydra, True)
        OmegaConf.set_struct(cfg, strict)

        # Merge all command line overrides after enabling strict flag
        all_consumed = consumed + consumed_free_job_defaults
        remaining_overrides = [x for x in overrides if x not in all_consumed]
        cfg.merge_with_dotlist(remaining_overrides)

        remaining = consumed + consumed_free_job_defaults + remaining_overrides

        def is_hydra(x):
            return x.startswith("hydra.") or x.startswith("hydra/")

        cfg.hydra.overrides.task = [x for x in remaining if not is_hydra(x)]
        cfg.hydra.overrides.hydra = [x for x in remaining if is_hydra(x)]

        with open_dict(cfg.hydra.job):
            if "name" not in cfg.hydra.job:
                cfg.hydra.job.name = JobRuntime().get("name")
            cfg.hydra.job.override_dirname = get_overrides_dirname(
                input_list=cfg.hydra.overrides.task,
                kv_sep=cfg.hydra.job.config.override_dirname.kv_sep,
                item_sep=cfg.hydra.job.config.override_dirname.item_sep,
                exclude_keys=cfg.hydra.job.config.override_dirname.exclude_keys,
            )
            cfg.hydra.job.config_file = config_file

        return cfg

    def load_sweep_config(self, master_config, sweep_overrides):
        # Recreate the config for this sweep instance with the appropriate overrides
        overrides = (
            OmegaConf.to_container(master_config.hydra.overrides.hydra)
            + sweep_overrides
        )
        sweep_config = self.load_configuration(
            config_file=master_config.hydra.job.config_file,
            strict=self.default_strict,
            overrides=overrides,
        )

        with open_dict(sweep_config):
            sweep_config.hydra.runtime.merge_with(master_config.hydra.runtime)

        # Copy old config cache to ensure we get the same resolved values (for things like timestamps etc)
        OmegaConf.copy_cache(from_config=master_config, to_config=sweep_config)

        return sweep_config

    def exists_in_search_path(self, filepath):
        _filename, search_path = self._find_config(filepath)
        return search_path is not None

    @staticmethod
    def exists(filename):
        is_pkg, path = ConfigLoader._split_path(filename)
        return ConfigLoader._exists(is_pkg, path)

    def get_search_path(self):
        return self.config_search_path

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

    def _find_config(self, filepath):
        found_search_path = None
        for search_path in self.config_search_path.config_search_path:
            is_pkg, path = self._split_path(search_path.path)
            config_file = "{}/{}".format(path, filepath)
            if self._exists(is_pkg, config_file):
                found_search_path = search_path
                break
        return filepath, found_search_path

    @staticmethod
    def _apply_defaults_overrides(overrides, defaults):
        consumed = []
        key_to_idx = {}
        for idx, d in enumerate(defaults):
            if isinstance(d, DictConfig):
                key = next(iter(d.keys()))
                key_to_idx[key] = idx
        for override in copy.deepcopy(overrides):
            key, value = split_key_val(override)
            if key in key_to_idx:
                if "," in value:
                    # If this is a multirun config (comma separated list), flag the default to prevent it from being
                    # loaded until we are constructing the config for individual jobs.
                    value = "_SKIP_"

                if value == "null":
                    del defaults[key_to_idx[key]]
                else:
                    defaults[key_to_idx[key]][key] = value

                overrides.remove(override)
                consumed.append(override)
        return consumed

    def _apply_free_defaults(self, defaults, overrides):
        consumed = []
        for override in copy.copy(overrides):
            key, value = split_key_val(override)
            if self.exists_in_search_path(key):
                # Do not add multirun configs into defaults, those will be added to the defaults
                # during the runs after list is broken into items
                if "," not in value:
                    defaults.append({key: value})
                overrides.remove(override)
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
        for d in copy.deepcopy(merged_list):
            if isinstance(d, (dict, DictConfig)):
                key = get_key(d)
                if key in key_to_idx.keys():
                    idx = key_to_idx[key]
                    primary[idx] = d
                    merged_list.remove(d)

        for d in merged_list:
            primary.append(d)

    def _load_config_impl(self, input_file, record_load=True):
        """
        :param input_file:
        :param record_load:
        :return: the loaded config or None if it was not found
        """
        loaded_cfg = None
        filename, search_path = self._find_config(input_file)
        if search_path is None and record_load:
            assert search_path is None
            self.all_config_checked.append((filename, None, None))

        if search_path is not None:
            fullpath = "{}/{}".format(search_path.path, filename)
            is_pkg = search_path.path.startswith("pkg://")
            if is_pkg:
                fullpath = fullpath[len("pkg://") :]
                module_name, resource_name = ConfigLoader._split_module_and_resource(
                    fullpath
                )
                with resource_stream(module_name, resource_name) as stream:
                    loaded_cfg = OmegaConf.load(stream)
                if record_load:
                    self.all_config_checked.append(
                        (filename, search_path.path, search_path.provider)
                    )
            elif os.path.exists(fullpath):
                loaded_cfg = OmegaConf.load(fullpath)
                if record_load:
                    self.all_config_checked.append(
                        (filename, search_path.path, search_path.provider)
                    )
            else:
                # This should never happen because we just searched for it and found it
                assert False, "'{}' not found".format(fullpath)
        return loaded_cfg

    def list_groups(self, parent_name):
        ret = list(set(self.get_group_options(parent_name, file_type="dir")))
        return ret

    def get_group_options(self, group_name, file_type="file"):
        options = []
        for search_path in self.config_search_path.config_search_path:
            search_path = search_path.path
            is_pkg, path = self._split_path(search_path)
            files = []
            if is_pkg:
                module_name, resource_name = ConfigLoader._split_module_and_resource(
                    "{}/{}".format(path, group_name)
                )
                if self._exists(is_pkg, path) and resource_isdir(
                    module_name, resource_name
                ):
                    all_files = resource_listdir(module_name, resource_name)
                    files = []
                    for file in all_files:
                        if (
                            file_type == "dir"
                            and resource_isdir(
                                module_name, os.path.join(group_name, file)
                            )
                            and file != "__pycache__"
                        ):
                            files.append(file)
                        elif file_type == "file" and file.endswith(".yaml"):
                            files.append(file[0 : -len(".yaml")])
            else:
                group_path = "{}/{}".format(path, group_name)
                if os.path.isdir(group_path):
                    all_files = os.listdir(group_path)
                    files = []
                    for file in all_files:
                        full_path = os.path.join(group_path, group_name, file)
                        if (
                            file_type == "dir"
                            and os.path.isdir(full_path)
                            and file != "__pycache__"
                        ):
                            files.append(file)
                        elif file_type == "file" and file.endswith(".yaml"):
                            files.append(file[0 : -len(".yaml")])

            options.extend(files)
        return options

    def _merge_config(self, cfg, family, name, required):

        if family != "":
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
                    options = self.get_group_options(family)
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
                ret = resource_exists(module_name, resource_name)
            except ImportError:
                ret = False
            except ValueError:  # Python 2.7 throws ValueError empty module name sometimes.
                ret = False
            except NotImplementedError:
                raise NotImplementedError(
                    "Unable to load {}/{}, are you missing an __init__.py?".format(
                        module_name, resource_name
                    )
                )
            # Uncomment to debug issues with configs not getting loaded.
            # WARNING: breaks integration tests that relies on specified output from the process.
            # print("_exists? {}, {} == {}".format(module_name, resource_name, ret))
            return ret
        else:
            return os.path.exists(filename)

    def _merge_defaults(self, cfg, defaults, split_at):
        def get_filename(config_name):
            filename, ext = os.path.splitext(config_name)
            if ext not in (".yaml", ".yml"):
                config_name = "{}{}".format(config_name, ".yaml")
            return config_name

        def merge_defaults(merged_cfg, def_list):
            cfg_with_list = OmegaConf.create(dict(defaults=def_list))
            for default1 in cfg_with_list.defaults:
                if isinstance(default1, DictConfig):
                    is_optional = False
                    if default1.optional is not None:
                        is_optional = default1.optional
                        del default1["optional"]
                    family = next(iter(default1.keys()))
                    name = default1[family]
                    # Name is none if default value is removed
                    if name is not None and "_SKIP_" not in name:
                        merged_cfg = self._merge_config(
                            cfg=merged_cfg,
                            family=family,
                            name=get_filename(name),
                            required=not is_optional,
                        )
                else:
                    assert isinstance(default1, str)
                    if "_SKIP_" not in default1:
                        merged_cfg = self._merge_config(
                            cfg=merged_cfg,
                            family="",
                            name=get_filename(default1),
                            required=True,
                        )
            return merged_cfg

        system_list = []
        user_list = []
        for default in defaults:
            if len(system_list) < split_at:
                system_list.append(default)
            else:
                user_list.append(default)
        cfg = merge_defaults(cfg, system_list)
        cfg = merge_defaults(cfg, user_list)

        if "defaults" in cfg:
            del cfg["defaults"]
        return cfg

    def _create_cfg(self, cfg_filename, record_load=True):
        if cfg_filename is None:
            cfg = OmegaConf.create()
        else:
            cfg = self._load_config_impl(cfg_filename, record_load=record_load)
            if cfg is None:
                raise IOError(
                    "could not find {}, config path:\n\t".format(
                        cfg_filename,
                        "\n\t".join(self.config_search_path.config_search_path),
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
