# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""
import copy
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from omegaconf import DictConfig, ListConfig, OmegaConf, open_dict
from omegaconf.errors import OmegaConfBaseException

from hydra._internal.config_repository import ConfigRepository
from hydra.core.config_loader import ConfigLoader, LoadTrace
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.errors import HydraException
from hydra.core.object_type import ObjectType
from hydra.core.utils import JobRuntime, get_overrides_dirname
from hydra.errors import MissingConfigException
from hydra.plugins.config_source import ConfigLoadError, ConfigSource


@dataclass
class ParsedOverride:
    key: str
    pkg1: Optional[str]
    pkg2: Optional[str]
    value: str

    def _get_subject_package(self) -> Optional[str]:
        return self.pkg1 if self.pkg2 is None else self.pkg2

    def _is_package_rename(self) -> bool:
        return self.pkg1 is not None and self.pkg2 is not None

    def _is_default_deletion(self) -> bool:
        return self.value == "null"


@dataclass
class DefaultElement:
    config_group: Optional[str]
    config_name: str
    optional: bool = False
    package: Optional[str] = None

    def __repr__(self) -> str:
        ret = ""
        if self.config_group is not None:
            ret += self.config_group
        if self.package is not None:
            ret += f"@{self.package}"
        ret += f"={self.config_name}"
        if self.optional:
            ret += " (optional)"
        return ret


@dataclass
class IndexedDefaultElement:
    idx: int
    default: DefaultElement

    def __repr__(self) -> str:
        return f"#{self.idx} : {self.default}"


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
        hydra_cfg, _load_trace = self._load_primary_config(cfg_filename="hydra_config")

        # Load job config
        job_cfg, job_cfg_load_trace = self._load_primary_config(
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

        self._combine_default_lists(defaults, job_defaults)
        consumed = self._apply_overrides_to_defaults(overrides, defaults)

        # Load and defaults and merge them into cfg
        cfg = self._merge_defaults_into_config(
            hydra_cfg, job_cfg, job_cfg_load_trace, defaults, split_at
        )
        OmegaConf.set_struct(cfg.hydra, True)
        OmegaConf.set_struct(cfg, strict)

        # Merge all command line overrides after enabling strict flag
        remaining_overrides = [x for x in overrides if x not in consumed]
        try:
            merged = OmegaConf.merge(cfg, OmegaConf.from_dotlist(remaining_overrides))
            assert isinstance(merged, DictConfig)
            cfg = merged
        except OmegaConfBaseException as ex:
            raise HydraException("Error merging overrides") from ex

        remaining = consumed + remaining_overrides

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

    def _apply_overrides_to_defaults(
        self, overrides: List[str], defaults: List[DefaultElement]
    ) -> List[str]:
        def is_matching(override: ParsedOverride, default: DefaultElement) -> bool:
            assert override.key == default.config_group
            if override._is_default_deletion():
                return override._get_subject_package() == default.package
            elif override._is_package_rename():
                return override.pkg1 == default.package
            else:
                return default.package is None

        def find_matches(
            key_to_defaults: Dict[str, List[IndexedDefaultElement]],
            override: ParsedOverride,
        ) -> List[IndexedDefaultElement]:
            matches: List[IndexedDefaultElement] = []
            for idefault in key_to_defaults[override.key]:
                if is_matching(override, idefault.default):
                    if override._is_package_rename():
                        for candidate in key_to_defaults[override.key]:
                            if candidate.default.package == override.pkg1:
                                matches.append(candidate)
                    else:
                        matches.append(idefault)
            return matches

        consumed = []
        key_to_defaults: Dict[str, List[IndexedDefaultElement]] = defaultdict(list)

        for idx, default in enumerate(defaults):
            if default.config_group is not None:
                key_to_defaults[default.config_group].append(
                    IndexedDefaultElement(idx=idx, default=default)
                )
        # copying overrides list because the loop is mutating it.
        for override_str in copy.deepcopy(overrides):
            override = ConfigLoaderImpl._parse_override(override_str)
            if not self.exists_in_search_path(override.key):
                continue

            if "," in override.value:
                # If this is a multirun config (comma separated list), flag the default to prevent it from being
                # loaded until we are constructing the config for individual jobs.
                override.value = "_SKIP_"

            if override.value == "null":
                matches = find_matches(key_to_defaults, override)
                for pair in matches:
                    del defaults[pair.idx]
            else:
                matches = find_matches(key_to_defaults, override)

                for match in matches:
                    default = match.default
                    default.config_name = override.value
                    if override.pkg1 is not None:
                        default.package = override._get_subject_package()
                if len(matches) == 0 and not (
                    override._is_package_rename() or override._is_default_deletion()
                ):
                    defaults.append(
                        DefaultElement(
                            config_group=override.key,
                            config_name=override.value,
                            package=override._get_subject_package(),
                        )
                    )

            consumed.append(override_str)
            overrides.remove(override_str)
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
    def _parse_override(override: str) -> ParsedOverride:
        # forms:
        # key=value
        # key@pkg=value
        # key@src_pkg:dst_pkg=value
        # regex code and tests: https://regex101.com/r/LiV6Rf/10

        regex = (
            r"^(?P<key>[A-Za-z0-9_.-/]+)(?:@(?P<pkg1>[A-Za-z0-9_\.-]*)"
            r"(?::(?P<pkg2>[A-Za-z0-9_\.-]*)?)?)?=(?P<value>.*)$"
        )
        matches = re.search(regex, override)

        if matches:
            key = matches.group("key")
            pkg1 = matches.group("pkg1")
            pkg2 = matches.group("pkg2")
            value = matches.group("value")
            return ParsedOverride(key, pkg1, pkg2, value)
        else:
            raise HydraException(
                f"Error parsing command line override : '{override}'\n"
                f"Accepted forms:\n"
                f"\tkey=value\n"
                f"\tkey@dest_pkg=value\n"
                f"\tkey@src_pkg:dest_pkg=value"
            )

    @staticmethod
    def _combine_default_lists(
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
        self,
        input_file: str,
        package_override: Optional[str],
        is_primary_config: bool,
        record_load: bool = True,
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
            config_path=input_file,
            is_primary_config=is_primary_config,
            package_override=package_override,
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
                        config_path,
                        is_primary_config=is_primary_config,
                        package_override=package_override,
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
        is_primary_config: bool,
        package_override: Optional[str],
    ) -> DictConfig:
        try:
            if config_group != "":
                new_cfg = f"{config_group}/{name}"
            else:
                new_cfg = name

            loaded_cfg, _ = self._load_config_impl(
                new_cfg,
                is_primary_config=is_primary_config,
                package_override=package_override,
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

    def _merge_defaults_into_config(
        self,
        hydra_cfg: DictConfig,
        job_cfg: DictConfig,
        job_cfg_load_trace: Optional[LoadTrace],
        defaults: List[DefaultElement],
        split_at: int,
    ) -> DictConfig:
        def merge_defaults_list_into_config(
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
                            is_primary_config=False,
                            package_override=default1.package,
                        )
                else:
                    if default1.config_name != "_SKIP_":
                        merged_cfg = self._merge_config(
                            cfg=merged_cfg,
                            config_group="",
                            name=config_name,
                            required=True,
                            is_primary_config=False,
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
        hydra_cfg = merge_defaults_list_into_config(hydra_cfg, system_list)
        hydra_cfg = merge_defaults_list_into_config(hydra_cfg, user_list)

        if "defaults" in hydra_cfg:
            del hydra_cfg["defaults"]
        return hydra_cfg

    def _load_primary_config(
        self, cfg_filename: Optional[str], record_load: bool = True
    ) -> Tuple[DictConfig, Optional[LoadTrace]]:
        if cfg_filename is None:
            cfg = OmegaConf.create()
            assert isinstance(cfg, DictConfig)
            load_trace = None
        else:
            ret, load_trace = self._load_config_impl(
                cfg_filename,
                is_primary_config=True,
                package_override=None,
                record_load=record_load,
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
