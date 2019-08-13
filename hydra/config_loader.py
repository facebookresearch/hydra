# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""

import copy
import os

from pkg_resources import resource_stream, resource_exists

# resource_listdir('hydra.default_conf','launcher')
from omegaconf import OmegaConf, DictConfig, ListConfig
from .errors import MissingConfigException
from .utils import JobRuntime


class ConfigLoader:
    """
    Configuration loader
    """

    # TODO: rename strict_task_cfg to strict_cfg
    def __init__(self, conf_filename, strict_task_cfg, config_path=[]):
        self.config_path = config_path
        self.conf_filename = conf_filename
        self.all_config_checked = []
        self.strict_task_cfg = strict_task_cfg

    def get_load_history(self):
        """
        returns the load history (which configs were attempted to load, and if they
        were loaded successfully or not.
        """
        return copy.deepcopy(self.all_config_checked)

    def find_config(self, filepath):
        for path in self.config_path:
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
        if self.conf_filename is None:
            task_cfg = OmegaConf.create()
        else:
            if self.find_config(self.conf_filename) is None:
                raise MissingConfigException(self.conf_filename)
            task_cfg, _consumed_defaults = self._create_cfg(
                cfg_filename=self.conf_filename,
                cli_overrides=job_overrides,
                strict=self.strict_task_cfg,
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
            cfg_filename="default_hydra.yaml", strict=False
        )
        dot_hydra = self.find_config(".hydra/hydra.yaml")
        consumed_defaults = []
        if dot_hydra is not None:
            hydra_cfg, consumed_defaults = self._create_cfg(
                cfg_filename=".hydra/hydra.yaml",
                strict=False,
                cli_overrides=overrides,
                defaults_only=True,
            )
        else:
            hydra_cfg = OmegaConf.from_dotlist(overrides)
        hydra_cfg = OmegaConf.merge(hydra_cfg_defaults, hydra_cfg)
        for consumed in consumed_defaults:
            hydra_cfg.hydra.overrides.hydra.append(consumed)
            overrides.remove(consumed)

        # strip everything outside of the hydra tree from the hydra config
        clean = OmegaConf.create()
        clean.hydra = hydra_cfg.hydra
        hydra_cfg = clean

        return hydra_cfg

    def _load_config_impl(self, input_file):
        loaded_cfg = None
        filename = self.find_config(input_file)
        if filename is None:
            self.all_config_checked.append((input_file, False))
        else:
            is_pkg = filename.startswith("pkg://")
            if is_pkg:
                filename = filename[len("pkg://") :]
                res_path = os.path.dirname(
                    filename
                )  # .replace("/", ".").replace("\\", ".")
                res_file = os.path.basename(filename)
                loaded_cfg = OmegaConf.load(resource_stream(res_path, res_file))
                self.all_config_checked.append(("pkg://" + filename, True))
            elif os.path.exists(filename):
                loaded_cfg = OmegaConf.load(filename)
                self.all_config_checked.append((filename, True))
            else:
                assert False

        return loaded_cfg

    def _merge_config(self, cfg, family, name, required):
        if family != ".":
            new_cfg = os.path.join(family, name)
        else:
            new_cfg = name

        loaded_cfg = self._load_config_impl(new_cfg)
        if loaded_cfg is None:
            # TODO: output possibilities
            if required:
                raise IOError("config not found " + new_cfg)
            else:
                return cfg

            # if self._exists(is_pkg, family_dir):
            #     options = [
            #         f[0: -len(".yaml")]
            #         for f in os.listdir(family_dir)
            #         if os.path.isfile(os.path.join(family_dir, f))
            #            and f.endswith(".yaml")
            #     ]
            #     msg = "Could not load {}, available options:\n{}:\n\t{}".format(
            #         cfg_path, family, "\n\t".join(options)
            #     )
            # else:
            #     options = None
            #     msg = "Could not load {}, directory not found".format(
            #         cfg_path, family
            #     )
            # raise MissingConfigException(msg, cfg_path, options)
        else:
            return OmegaConf.merge(cfg, loaded_cfg)

    @staticmethod
    def _exists(is_pkg, filename):
        if is_pkg:
            res_base = os.path.dirname(filename)
            res_file = os.path.basename(filename)
            try:
                return resource_exists(res_base, res_file)
            except ImportError:
                return False
        else:
            return os.path.exists(filename)

    def _create_cfg(self, cfg_filename, strict, cli_overrides=[], defaults_only=False):
        if cfg_filename is None:
            return OmegaConf.create(), []

        main_cfg = self._load_config_impl(cfg_filename)
        if main_cfg is None:
            raise IOError(
                "could not find {}, config path:\n\t".format(
                    cfg_filename, "\n\t".join(self.config_path)
                )
            )

        conf_dirname = os.path.dirname(cfg_filename)

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

            if self.find_config(os.path.join(key, value)) is not None:
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
                )
            else:
                assert isinstance(default, str)
                cfg = self._merge_config(
                    cfg=cfg, family=conf_dirname, name=default, required=True
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
