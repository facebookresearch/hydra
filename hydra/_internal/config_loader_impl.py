# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""
import copy
import os
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from omegaconf import DictConfig, ListConfig, OmegaConf, open_dict
from omegaconf.errors import OmegaConfBaseException

from hydra._internal.config_repository import ConfigRepository
from hydra.core.config_loader import ConfigLoader, LoadTrace
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.errors import HydraException
from hydra.core.object_type import ObjectType
from hydra.core.utils import JobRuntime, get_overrides_dirname, split_key_val
from hydra.errors import MissingConfigException
from hydra.plugins.config_source import ConfigLoadError, ConfigSource


@dataclass
class DefaultElement:
    config_group: Optional[str]
    config_name: str
    optional: bool = False
    package: Optional[str] = None


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
        if strict is None:
            strict = self.default_strict

        overrides = copy.deepcopy(overrides) or []

        if config_name is not None and not self.exists_in_search_path(config_name):
            # TODO: handle schema as a special case
            descs = [
                f"\t{src.path} (from {src.provider})"
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

        job_defaults = self._parse_defaults(job_cfg)
        defaults = self._parse_defaults(hydra_cfg)

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
            defaults.append(DefaultElement(config_group=None, config_name="__SELF__"))
        split_at = len(defaults)

        self._merge_default_lists(defaults, job_defaults)
        consumed = self._apply_overrides_to_defaults(overrides, defaults)

        consumed_free_job_defaults = self._append_free_config_group_overrides_to_defaults(
            defaults, overrides
        )

        # Load and defaults and merge them into cfg
        cfg = self._merge_defaults(
            hydra_cfg, job_cfg, job_cfg_load_trace, defaults, split_at
        )
        OmegaConf.set_struct(cfg.hydra, True)
        OmegaConf.set_struct(cfg, strict)

        # Merge all command line overrides after enabling strict flag
        all_consumed = consumed + consumed_free_job_defaults
        remaining_overrides = [x for x in overrides if x not in all_consumed]
        try:
            merged = OmegaConf.merge(cfg, OmegaConf.from_dotlist(remaining_overrides))
            assert isinstance(merged, DictConfig)
            cfg = merged
        except OmegaConfBaseException as ex:
            raise HydraException("Error merging overrides") from ex

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

            for key in cfg.hydra.job.env_copy:
                cfg.hydra.job.env_set[key] = os.environ[key]

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
    def _apply_overrides_to_defaults(
        overrides: List[str], defaults: List[DefaultElement]
    ) -> List[str]:
        consumed = []
        key_to_idx = {}
        for idx, d in enumerate(defaults):
            if d.config_group is not None:
                key_to_idx[d.config_group] = idx
        for override in copy.deepcopy(overrides):
            group, package, value = ConfigLoaderImpl._split_override(override)
            if group in key_to_idx:
                if "," in value:
                    # If this is a multirun config (comma separated list), flag the default to prevent it from being
                    # loaded until we are constructing the config for individual jobs.
                    value = "_SKIP_"

                if value == "null":
                    del defaults[key_to_idx[group]]
                else:
                    default = defaults[key_to_idx[group]]
                    default.config_name = value
                    if package is not None:
                        default.package = package

                overrides.remove(override)
                consumed.append(override)
        return consumed

    @staticmethod
    def _split_group(group_with_package: str) -> Tuple[str, Optional[str]]:
        idx = group_with_package.find("@")
        if idx == -1:
            # group
            group = group_with_package
            package = None
        else:
            # group@package
            group = group_with_package[0:idx]
            package = group_with_package[idx + 1 :]

        return group, package

    @staticmethod
    def _split_override(override: str) -> Tuple[str, Optional[str], str]:
        idx = override.find("@")
        if idx == -1:
            # key=value
            group, value = split_key_val(override)
            package = None
        else:
            # key@package=value
            group = override[0:idx]
            eq_idx = override.find("=", idx)
            if eq_idx == -1:
                raise ValueError(
                    f"'{override}' not a valid override, expecting key=value or key@package=value format"
                )

            package = override[idx + 1 : eq_idx]
            value = override[eq_idx + 1 :]

        return group, package, value

    def _append_free_config_group_overrides_to_defaults(
        self, defaults: List[DefaultElement], overrides: List[str]
    ) -> List[str]:
        consumed = []
        for override in copy.copy(overrides):
            group, package, value = self._split_override(override)
            if self.exists_in_search_path(group):
                # Do not add multirun configs into defaults, those will be added to the defaults
                # during the runs after list is broken into items
                if "," not in value:
                    if package is None:
                        defaults.append(
                            DefaultElement(config_group=group, config_name=value)
                        )
                    else:
                        defaults.append(
                            DefaultElement(
                                config_group=group, config_name=value, package=package
                            )
                        )
                overrides.remove(override)
                consumed.append(override)

        return consumed

    @staticmethod
    def _merge_default_lists(
        primary: List[DefaultElement], merged_list: List[DefaultElement]
    ) -> None:
        key_to_idx = {}
        for idx, d in enumerate(primary):
            if d.config_group is not None:
                key_to_idx[d.config_group] = idx
        for d in copy.deepcopy(merged_list):
            if d.config_group is not None:
                if d.config_group in key_to_idx.keys():
                    idx = key_to_idx[d.config_group]
                    primary[idx] = d
                    merged_list.remove(d)

        # append remaining items that were not matched to existing keys
        for d in merged_list:
            primary.append(d)

    def _load_config_impl(
        self, input_file: str, package_override: Optional[str], record_load: bool = True
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

        ret = self.repository.load_config(
            config_path=input_file, package_override=package_override
        )

        if ret is not None:
            if not isinstance(ret.config, DictConfig):
                raise ValueError(
                    f"Config {input_file} must be a Dictionary, got {type(ret).__name__}"
                )
            if not ret.is_schema_source:
                try:
                    schema_source = self.repository.get_schema_source()
                    config_path = ConfigSource._normalize_file_name(filename=input_file)
                    schema = schema_source.load_config(
                        config_path, package_override=package_override
                    )

                    merged = OmegaConf.merge(schema.config, ret.config)
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
        self,
        cfg: DictConfig,
        config_group: str,
        name: str,
        required: bool,
        package_override: Optional[str],
    ) -> DictConfig:
        try:
            if config_group != "":
                new_cfg = f"{config_group}/{name}"
            else:
                new_cfg = name

            loaded_cfg, _ = self._load_config_impl(
                new_cfg, package_override=package_override
            )
            if loaded_cfg is None:
                if required:
                    if config_group == "":
                        msg = f"Could not load {new_cfg}"
                        raise MissingConfigException(msg, new_cfg)
                    else:
                        options = self.get_group_options(config_group)
                        if options:
                            lst = "\n\t".join(options)
                            msg = f"Could not load {new_cfg}, available options:\n{config_group}:\n\t{lst}"
                        else:
                            msg = f"Could not load {new_cfg}"
                        raise MissingConfigException(msg, new_cfg, options)
                else:
                    return cfg

            else:
                ret = OmegaConf.merge(cfg, loaded_cfg)
                assert isinstance(ret, DictConfig)
                return ret
        except OmegaConfBaseException as ex:
            raise HydraException(f"Error merging {config_group}={name}") from ex

    def _merge_defaults(
        self,
        hydra_cfg: DictConfig,
        job_cfg: DictConfig,
        job_cfg_load_trace: Optional[LoadTrace],
        defaults: List[DefaultElement],
        split_at: int,
    ) -> DictConfig:
        def merge_defaults(
            merged_cfg: DictConfig, def_list: List[DefaultElement]
        ) -> DictConfig:
            # Reconstruct the defaults to make use of the interpolation capabilities of OmegaConf.
            dict_with_list = OmegaConf.create({"defaults": []})
            for item in def_list:
                d: Any
                if item.config_group is not None:
                    d = {item.config_group: item.config_name}
                else:
                    d = item.config_name
                dict_with_list.defaults.append(d)

            for idx, default1 in enumerate(def_list):
                if default1.config_group is not None:
                    config_name = dict_with_list.defaults[idx][default1.config_group]
                else:
                    config_name = dict_with_list.defaults[idx]

                if config_name == "__SELF__":
                    if "defaults" in job_cfg:
                        with open_dict(job_cfg):
                            del job_cfg["defaults"]
                    merged_cfg.merge_with(job_cfg)
                    if job_cfg_load_trace is not None:
                        self.all_config_checked.append(job_cfg_load_trace)
                elif default1.config_group is not None:
                    if default1.config_name not in (None, "_SKIP_"):
                        merged_cfg = self._merge_config(
                            cfg=merged_cfg,
                            config_group=default1.config_group,
                            name=config_name,
                            required=not default1.optional,
                            package_override=default1.package,
                        )
                else:
                    if default1.config_name != "_SKIP_":
                        merged_cfg = self._merge_config(
                            cfg=merged_cfg,
                            config_group="",
                            name=config_name,
                            required=True,
                            package_override=default1.package,
                        )
            return merged_cfg

        system_list: List[DefaultElement] = []
        user_list: List[DefaultElement] = []
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
                cfg_filename, package_override=None, record_load=record_load
            )
            assert ret is not None
            cfg = ret

        return cfg, load_trace

    @staticmethod
    def _parse_defaults(cfg: DictConfig) -> List[DefaultElement]:
        valid_example = """
        Example of a valid defaults:
        defaults:
          - dataset: imagenet
          - model: alexnet
            optional: true
          - optimizer: nesterov
        """

        if "defaults" in cfg:
            defaults = cfg.defaults
        else:
            defaults = OmegaConf.create([])

        if not isinstance(defaults, ListConfig):
            raise ValueError(
                "defaults must be a list because composition is order sensitive, "
                + valid_example
            )

        assert isinstance(defaults, ListConfig)

        res: List[DefaultElement] = []
        for item in defaults:
            if isinstance(item, DictConfig):
                optional = False
                if "optional" in item:
                    optional = item.pop("optional")
                keys = list(item.keys())
                if len(keys) > 1:
                    raise ValueError(f"Too many keys in default item {item}")
                if len(keys) == 0:
                    raise ValueError(f"Missing group name in {item}")
                key = keys[0]
                config_group, package = ConfigLoaderImpl._split_group(key)
                node = item._get_node(key)
                assert node is not None
                config_name = node._value()

                default = DefaultElement(
                    config_group=config_group,
                    config_name=config_name,
                    package=package,
                    optional=optional,
                )
            elif isinstance(item, str):
                default = DefaultElement(config_group=None, config_name=item)
            else:
                raise ValueError(
                    f"Unsupported type in defaults : {type(item).__name__}"
                )
            res.append(default)

        return res

    def get_sources(self) -> List[ConfigSource]:
        return self.repository.get_sources()
