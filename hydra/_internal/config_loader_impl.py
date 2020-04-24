# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""
import copy
from typing import List, Optional, Tuple

from omegaconf import DictConfig, ListConfig, OmegaConf, open_dict

from hydra._internal.config_repository import ConfigRepository
from hydra.core.config_loader import ConfigLoader, LoadTrace
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.config_store import ConfigStore
from hydra.core.object_type import ObjectType
from hydra.core.utils import JobRuntime, get_overrides_dirname, split_key_val
from hydra.errors import MissingConfigException
from hydra.plugins.config_source import ConfigLoadError, ConfigSource


class ConfigLoaderImpl(ConfigLoader):
    """
    Configuration loader
    """

    def __init__(
        self,
        config_search_path: ConfigSearchPath,
        default_strict: Optional[bool] = None,
    ) -> None:
        self.default_strict = default_strict
        self.all_config_checked: List[LoadTrace] = []
        self.config_search_path = config_search_path
        self.repository: ConfigRepository = ConfigRepository(
            config_search_path=config_search_path
        )

    def load_configuration(
        self,
        config_name: Optional[str],
        overrides: List[str],
        strict: Optional[bool] = None,
    ) -> DictConfig:
        assert config_name is None or isinstance(config_name, str)
        assert strict is None or isinstance(strict, bool)
        assert isinstance(overrides, list)
        if strict is None:
            strict = self.default_strict

        assert overrides is None or isinstance(overrides, list)
        overrides = copy.deepcopy(overrides) or []

        if config_name is not None and not self.exists_in_search_path(config_name):
            # TODO: handle schema as a special case
            descs = [
                "\t{} (from {})".format(src.path, src.provider)
                for src in self.repository.get_sources()
            ]
            lines = "\n".join(descs)
            raise MissingConfigException(
                missing_cfg_file=config_name,
                message=f"Cannot find primary config file: {config_name}\nSearch path:\n{lines}",
            )

        # Load hydra config
        hydra_cfg, _load_trace = self._create_cfg(cfg_filename="hydra_config")

        # Load job config
        job_cfg, job_cfg_load_trace = self._create_cfg(
            cfg_filename=config_name, record_load=False
        )

        job_defaults = ConfigLoaderImpl._get_defaults(job_cfg)
        defaults = ConfigLoaderImpl._get_defaults(hydra_cfg)

        job_cfg_type = OmegaConf.get_type(job_cfg)
        if job_cfg_type is not None and not issubclass(job_cfg_type, dict):
            hydra_cfg._promote(job_cfg_type)
            # this is breaking encapsulation a bit. can potentially be implemented in OmegaConf
            hydra_cfg._metadata.ref_type = job_cfg._metadata.ref_type

        # if defaults are re-introduced by the promotion, remove it.
        if "defaults" in hydra_cfg:
            with open_dict(hydra_cfg):
                del hydra_cfg["defaults"]

        if config_name is not None:
            defaults.append("__SELF__")
        split_at = len(defaults)

        ConfigLoaderImpl._merge_default_lists(defaults, job_defaults)
        consumed = self._apply_defaults_overrides(overrides, defaults)

        consumed_free_job_defaults = self._apply_free_defaults(defaults, overrides)

        ConfigLoaderImpl._validate_defaults(defaults)

        # Load and defaults and merge them into cfg
        cfg = self._merge_defaults(
            hydra_cfg, job_cfg, job_cfg_load_trace, defaults, split_at
        )
        OmegaConf.set_struct(cfg.hydra, True)
        OmegaConf.set_struct(cfg, strict)

        # Merge all command line overrides after enabling strict flag
        all_consumed = consumed + consumed_free_job_defaults
        remaining_overrides = [x for x in overrides if x not in all_consumed]
        cfg.merge_with_dotlist(remaining_overrides)

        remaining = consumed + consumed_free_job_defaults + remaining_overrides

        def is_hydra(x: str) -> bool:
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
            cfg.hydra.job.config_name = config_name

        return cfg

    def load_sweep_config(
        self, master_config: DictConfig, sweep_overrides: List[str]
    ) -> DictConfig:
        # Recreate the config for this sweep instance with the appropriate overrides
        overrides = OmegaConf.to_container(master_config.hydra.overrides.hydra)
        assert isinstance(overrides, list)
        overrides = overrides + sweep_overrides
        sweep_config = self.load_configuration(
            config_name=master_config.hydra.job.config_name,
            strict=self.default_strict,
            overrides=overrides,
        )

        with open_dict(sweep_config):
            sweep_config.hydra.runtime.merge_with(master_config.hydra.runtime)

        # Copy old config cache to ensure we get the same resolved values (for things like timestamps etc)
        OmegaConf.copy_cache(from_config=master_config, to_config=sweep_config)

        return sweep_config

    def exists_in_search_path(self, filepath: str) -> bool:
        return self.repository.exists(filepath)

    def get_search_path(self) -> ConfigSearchPath:
        return self.config_search_path

    def get_load_history(self) -> List[LoadTrace]:
        """
        returns the load history (which configs were attempted to load, and if they
        were loaded successfully or not.
        """
        return copy.deepcopy(self.all_config_checked)

    @staticmethod
    def _apply_defaults_overrides(
        overrides: List[str], defaults: ListConfig
    ) -> List[str]:
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

    def _apply_free_defaults(
        self, defaults: ListConfig, overrides: List[str]
    ) -> List[str]:
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
    def _merge_default_lists(primary: ListConfig, merged_list: ListConfig) -> None:
        assert isinstance(primary, ListConfig)
        assert isinstance(merged_list, ListConfig)

        def get_key(d1: DictConfig) -> str:
            keys_iter = iter(d1.keys())
            key1 = next(keys_iter)
            if key1 == "optional":
                key1 = next(keys_iter)
            assert isinstance(key1, str)
            return key1

        key_to_idx = {}
        for idx, d in enumerate(primary):
            assert isinstance(d, (DictConfig, str))
            if isinstance(d, DictConfig):
                key = get_key(d)
                key_to_idx[key] = idx
        for d in copy.deepcopy(merged_list):
            if isinstance(d, DictConfig):
                key = get_key(d)
                if key in key_to_idx.keys():
                    idx = key_to_idx[key]
                    primary[idx] = d
                    merged_list.remove(d)

        # append remaining items that were not matched to existing keys
        for d in merged_list:
            primary.append(d)

    def _load_config_impl(
        self, input_file: str, record_load: bool = True
    ) -> Tuple[Optional[DictConfig], Optional[LoadTrace]]:
        """
        :param input_file:
        :param record_load:
        :return: the loaded config or None if it was not found
        """

        def record_loading(
            name: str,
            path: Optional[str],
            provider: Optional[str],
            schema_provider: Optional[str],
        ) -> Optional[LoadTrace]:
            trace = LoadTrace(
                filename=name,
                path=path,
                provider=provider,
                schema_provider=schema_provider,
            )

            if record_load:
                self.all_config_checked.append(trace)

            return trace

        ret = self.repository.load_config(config_path=input_file)

        if ret is not None:
            if not isinstance(ret.config, DictConfig):
                raise ValueError(
                    f"Config {input_file} must be a Dictionary, got {type(ret).__name__}"
                )
            if not ret.is_schema_source:
                try:
                    schema = ConfigStore.instance().load(
                        config_path=ConfigSource._normalize_file_name(
                            filename=input_file
                        )
                    )

                    merged = OmegaConf.merge(schema.node, ret.config)
                    assert isinstance(merged, DictConfig)
                    return (
                        merged,
                        record_loading(
                            name=input_file,
                            path=ret.path,
                            provider=ret.provider,
                            schema_provider=schema.provider,
                        ),
                    )

                except ConfigLoadError:
                    # schema not found, ignore
                    pass

            return (
                ret.config,
                record_loading(
                    name=input_file,
                    path=ret.path,
                    provider=ret.provider,
                    schema_provider=None,
                ),
            )
        else:
            return (
                None,
                record_loading(
                    name=input_file, path=None, provider=None, schema_provider=None
                ),
            )

    def list_groups(self, parent_name: str) -> List[str]:
        return self.get_group_options(
            group_name=parent_name, results_filter=ObjectType.GROUP
        )

    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        return self.repository.get_group_options(group_name, results_filter)

    def _merge_config(
        self, cfg: DictConfig, family: str, name: str, required: bool
    ) -> DictConfig:

        if family != "":
            new_cfg = "{}/{}".format(family, name)
        else:
            new_cfg = name

        loaded_cfg, _ = self._load_config_impl(new_cfg)
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
            ret = OmegaConf.merge(cfg, loaded_cfg)
            assert isinstance(ret, DictConfig)
            return ret

    def _merge_defaults(
        self,
        hydra_cfg: DictConfig,
        job_cfg: DictConfig,
        job_cfg_load_trace: Optional[LoadTrace],
        defaults: ListConfig,
        split_at: int,
    ) -> DictConfig:
        def merge_defaults(merged_cfg: DictConfig, def_list: ListConfig) -> DictConfig:
            cfg_with_list = OmegaConf.create(dict(defaults=def_list))
            for default1 in cfg_with_list.defaults:
                if default1 == "__SELF__":
                    merged_cfg.merge_with(job_cfg)
                    if job_cfg_load_trace is not None:
                        self.all_config_checked.append(job_cfg_load_trace)
                elif isinstance(default1, DictConfig):
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
                            name=name,
                            required=not is_optional,
                        )
                else:
                    assert isinstance(default1, str)
                    if "_SKIP_" not in default1:
                        merged_cfg = self._merge_config(
                            cfg=merged_cfg, family="", name=default1, required=True
                        )
            return merged_cfg

        system_list: ListConfig = OmegaConf.create([])
        user_list: ListConfig = OmegaConf.create([])
        for default in defaults:
            if len(system_list) < split_at:
                system_list.append(default)
            else:
                user_list.append(default)
        hydra_cfg = merge_defaults(hydra_cfg, system_list)
        hydra_cfg = merge_defaults(hydra_cfg, user_list)

        if "defaults" in hydra_cfg:
            del hydra_cfg["defaults"]
        return hydra_cfg

    def _create_cfg(
        self, cfg_filename: Optional[str], record_load: bool = True
    ) -> Tuple[DictConfig, Optional[LoadTrace]]:
        if cfg_filename is None:
            cfg = OmegaConf.create()
            assert isinstance(cfg, DictConfig)
            load_trace = None
        else:
            ret, load_trace = self._load_config_impl(
                cfg_filename, record_load=record_load
            )
            assert ret is not None
            cfg = ret

        if "defaults" in cfg and cfg.defaults is not None:
            self._validate_defaults(cfg.defaults)

        return cfg, load_trace

    @staticmethod
    def _validate_defaults(defaults: ListConfig) -> None:

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
    def _get_defaults(cfg: DictConfig) -> ListConfig:
        valid_example = """
        Example of a valid defaults:
        defaults:
          - dataset: imagenet
          - model: alexnet
            optional: true
          - optimizer: nesterov
        """

        if "defaults" in cfg:
            with open_dict(cfg):
                defaults = cfg.pop("defaults")
        else:
            defaults = OmegaConf.create([])

        if not isinstance(defaults, ListConfig):
            raise ValueError(
                "defaults must be a list because composition is order sensitive, "
                + valid_example
            )

        assert isinstance(defaults, ListConfig)
        return defaults

    def get_sources(self) -> List[ConfigSource]:
        return self.repository.get_sources()
