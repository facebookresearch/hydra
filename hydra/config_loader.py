# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""

import copy
import os

from pkg_resources import (
    resource_stream,
    resource_exists,
    resource_listdir,
    resource_isdir,
)

from omegaconf import OmegaConf, DictConfig, ListConfig
from .errors import MissingConfigException
from .utils import JobRuntime


class ConfigLoader:
    """
    Configuration loader
    """

    # TODO: rename strict_task_cfg to strict_cfg
    def __init__(self, conf_filename, conf_dir, strict_task_cfg, config_path=[]):
        self.config_path = config_path
        self.conf_dir = conf_dir
        self.conf_filename = conf_filename
        self.all_config_checked = []
        self.strict_task_cfg = strict_task_cfg

    def get_load_history(self):
        """
        returns the load history (which configs were attempted to load, and if they
        were loaded successfully or not.
        """
        return copy.deepcopy(self.all_config_checked)

    def _is_group(self, group_name, including_config_dir):
        for path in self._get_config_path(including_config_dir):
            is_pkg = path.startswith("pkg://")
            if is_pkg:
                prefix = "pkg://"
                path = path[len(prefix) :]
                full_group_name = os.path.join(path, group_name)
                full_group_name = full_group_name.replace("/", ".").replace("\\", ".")
            else:
                full_group_name = os.path.join(path, group_name)

            if self._exists(is_pkg, full_group_name) is True:
                return True
        return False

    def _get_config_path(self, including_config_dir):
        config_path = copy.deepcopy(self.config_path)
        if including_config_dir and self.conf_dir is not None:
            config_path.append(self.conf_dir)
        return config_path

    def _find_config(self, filepath, including_config_dir):
        config_path = self._get_config_path(including_config_dir)
        for path in config_path:
            is_pkg = path.startswith("pkg://")
            prefix = ""
            if is_pkg:
                prefix = "pkg://"
                path = path[len(prefix) :]
                config_file = os.path.join(path, filepath)
                res_path = (
                    os.path.dirname(config_file).replace("/", ".").replace("\\", ".")
                )
                res_file = os.path.basename(config_file)
                config_file = os.path.join(res_path, res_file)
            else:
                config_file = os.path.join(path, filepath)

            if not config_file.endswith(".yaml"):
                config_file = config_file + ".yaml"

            if self._exists(is_pkg, config_file):
                return prefix + config_file
        return None

    def load_configuration(self, overrides=[]):
        assert overrides is None or isinstance(overrides, list)

        overrides = overrides or []
        hydra_cfg = self._load_hydra_cfg(overrides)

        job_overrides = [x for x in overrides if not x.startswith("hydra.")]
        hydra_overrides = [x for x in overrides if x.startswith("hydra.")]
        # if self.conf_filename is not None and self._find_config(self.conf_filename) is None:
        #     raise MissingConfigException("Can't config file {}".format(self.conf_filename), self.conf_filename)
        task_cfg, _consumed_defaults = self._create_cfg(
            cfg_filename=self.conf_filename,
            strict=self.strict_task_cfg,
            open_defaults=True,
            including_config_dir=True,
            cli_overrides=job_overrides,
        )
        cfg = OmegaConf.merge(hydra_cfg, task_cfg)

        for item in job_overrides:
            cfg.hydra.overrides.task.append(item)
        for item in hydra_overrides:
            cfg.hydra.overrides.hydra.append(item)

        job = OmegaConf.create(dict(name=JobRuntime().get("name")))
        cfg.hydra.job = OmegaConf.merge(job, cfg.hydra.job)
        OmegaConf.set_struct(cfg, self.strict_task_cfg)
        # Merge hydra overrides after combining both configs and applying the strict flag.
        cfg.merge_with_dotlist(hydra_overrides)
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
            cfg_filename="default_hydra.yaml",
            strict=False,
            including_config_dir=False,
            open_defaults=False,
        )
        hydra_cfg, consumed_defaults = self._create_cfg(
            cfg_filename=".hydra/hydra.yaml",
            strict=False,
            including_config_dir=True,
            cli_overrides=overrides,
            defaults_only=True,
            open_defaults=False,
        )
        hydra_cfg = OmegaConf.merge(hydra_cfg_defaults, hydra_cfg)
        for consumed in consumed_defaults:
            hydra_cfg.hydra.overrides.hydra.append(consumed)
            overrides.remove(consumed)

        # strip everything outside of the hydra tree from the hydra config
        clean = OmegaConf.create()
        clean.hydra = hydra_cfg.hydra
        hydra_cfg = clean

        return hydra_cfg

    def _load_config_impl(self, input_file, including_config_dir):
        loaded_cfg = None
        filename = self._find_config(input_file, including_config_dir)
        if filename is None:
            self.all_config_checked.append((input_file, False))
        else:
            is_pkg = filename.startswith("pkg://")
            if is_pkg:
                filename = filename[len("pkg://") :]
                res_path = os.path.dirname(filename)
                res_file = os.path.basename(filename)
                loaded_cfg = OmegaConf.load(resource_stream(res_path, res_file))
                self.all_config_checked.append(("pkg://" + filename, True))
            elif os.path.exists(filename):
                loaded_cfg = OmegaConf.load(filename)
                self.all_config_checked.append((filename, True))
            else:
                assert False

        return loaded_cfg

    def _get_group_options(self, group_name, including_config_dir):
        options = []
        for path in self._get_config_path(including_config_dir):
            is_pkg = path.startswith("pkg://")
            files = []
            if is_pkg:
                path = path[len("pkg://") :].replace("/", ".").replace("\\", ".")
                if resource_isdir(path, group_name):
                    files = resource_listdir(path, group_name)
            else:
                group_path = os.path.join(path, group_name)
                if os.path.isdir(group_path):
                    files = os.listdir(group_path)
            files = [f for f in files if f.endswith(".yaml")]
            files = [f[0 : -len(".yaml")] for f in files]
            options.extend(files)
        return options

    def _merge_config(self, cfg, family, name, required, including_config_dir):
        if family != ".":
            new_cfg = os.path.join(family, name)
        else:
            new_cfg = name

        loaded_cfg = self._load_config_impl(new_cfg, including_config_dir)
        if loaded_cfg is None:
            if required:
                if family == "":
                    msg = "Could not load {}".format(new_cfg)
                    raise MissingConfigException(msg, new_cfg)
                else:
                    options = self._get_group_options(family, including_config_dir)
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
        else:
            return os.path.exists(filename)

    def _create_cfg(
        self,
        cfg_filename,
        strict,
        including_config_dir,
        cli_overrides=[],
        defaults_only=False,
        open_defaults=True,
    ):
        """
        :param cfg_filename:
        :param strict:
        :param including_config_dir:
        :param cli_overrides:
        :param defaults_only:
        :param open_defaults: Allow adding loading additional keys to defaults.
        :return:
        """
        resolved_cfg_filename = (
            self._find_config(cfg_filename, including_config_dir)
            if cfg_filename is not None
            else None
        )
        if resolved_cfg_filename is None:
            main_cfg = OmegaConf.create()
            conf_dirname = "."
        else:
            # TODO: pass resolved_cfg_filename to load?
            main_cfg = self._load_config_impl(cfg_filename, including_config_dir)
            conf_dirname = os.path.dirname(cfg_filename)
            if main_cfg is None:
                raise IOError(
                    "could not find {}, config path:\n\t".format(
                        cfg_filename,
                        "\n\t".join(self._get_config_path(including_config_dir)),
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
            can_add = (
                open_defaults
                or key in main_cfg.defaults
                or {key: value} in main_cfg.defaults
            )
            if can_add and self._is_group(key, including_config_dir):
                # if self.find_config(os.path.join(key, value)) is not None:
                defaults_changes[key] = value
                consumed_defaults.append(override)
            else:
                overrides.append(override)

        ConfigLoader._update_defaults(main_cfg, defaults_changes)

        cfg = main_cfg
        for default in main_cfg.defaults:
            if isinstance(default, DictConfig):
                is_optional = False
                if default.optional is not None:
                    is_optional = default.optional
                    del default["optional"]
                family = next(iter(default.keys()))
                name = default[family]
                cfg = self._merge_config(
                    cfg=cfg,
                    family=os.path.join(conf_dirname, family),
                    name=name,
                    required=not is_optional,
                    including_config_dir=including_config_dir,
                )
            else:
                assert isinstance(default, str)
                cfg = self._merge_config(
                    cfg=cfg,
                    family=conf_dirname,
                    name=default,
                    required=True,
                    including_config_dir=including_config_dir,
                )

        if strict:
            OmegaConf.set_struct(cfg, True)

        # merge in remaining overrides
        if not defaults_only:
            cfg.merge_with_dotlist(overrides)
        # remove config block from resulting cfg.
        del cfg["defaults"]
        return cfg, consumed_defaults

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
        for default in cfg.defaults:
            if isinstance(default, DictConfig):
                for key in default.keys():
                    if key != "optional":
                        if key in defaults_changes:
                            default[key] = defaults_changes[key]
                            del defaults_changes[key]
        # unmatched new defaults, put at end of list to be loaded normally
        for key, value in defaults_changes.items():
            cfg.defaults.append({key: value})
