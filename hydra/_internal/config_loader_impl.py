# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""
import copy
import os
import re
import warnings
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import yaml
from omegaconf import DictConfig, ListConfig, OmegaConf, _utils, open_dict
from omegaconf.errors import (
    ConfigAttributeError,
    ConfigKeyError,
    OmegaConfBaseException,
)

from hydra._internal.config_repository import ConfigRepository
from hydra.core.config_loader import ConfigLoader, LoadTrace
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.object_type import ObjectType
from hydra.core.utils import JobRuntime
from hydra.errors import HydraException, MissingConfigException
from hydra.plugins.config_source import ConfigLoadError, ConfigSource


@dataclass
class ParsedConfigOverride:
    prefix: Optional[str]
    key: str
    value: Optional[str]

    def is_delete(self) -> bool:
        return self.prefix == "~"

    def is_add(self) -> bool:
        return self.prefix == "+"


@dataclass
class ParsedOverride:
    prefix: Optional[str]
    key: str
    pkg1: Optional[str]
    pkg2: Optional[str]
    value: Optional[str]

    def get_source_package(self) -> Optional[str]:
        return self.pkg1

    def get_subject_package(self) -> Optional[str]:
        return self.pkg1 if self.pkg2 is None else self.pkg2

    def get_source_item(self) -> str:
        pkg = self.get_source_package()
        if pkg is None:
            return self.key
        else:
            return f"{self.key}@{pkg}"

    def is_package_rename(self) -> bool:
        return self.pkg1 is not None and self.pkg2 is not None

    def is_delete(self) -> bool:
        legacy_delete = self.value == "null"
        return self.prefix == "~" or legacy_delete

    def is_add(self) -> bool:
        return self.prefix == "+"


@dataclass
class ParsedOverrideWithLine:
    override: ParsedOverride
    input_line: str


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

    def split_overrides(
        self, pairs: List[ParsedOverrideWithLine],
    ) -> Tuple[List[ParsedOverrideWithLine], List[ParsedOverrideWithLine]]:
        config_group_overrides = []
        config_overrides = []
        for pwd in pairs:
            if not self.repository.group_exists(pwd.override.key):
                config_overrides.append(pwd)
            else:
                config_group_overrides.append(pwd)
        return config_group_overrides, config_overrides

    def missing_config_error(
        self, config_name: Optional[str], msg: str, with_search_path: bool
    ) -> None:
        def add_search_path(msg: str) -> str:
            descs = []
            for src in self.repository.get_sources():
                if src.provider != "schema":
                    descs.append(f"\t{repr(src)}")
            lines = "\n".join(descs)

            if with_search_path:
                return msg + "\nSearch path:" + f"\n{lines}"
            else:
                return msg

        raise MissingConfigException(
            missing_cfg_file=config_name, message=add_search_path(msg)
        )

    def ensure_main_config_source_available(self) -> None:
        for source in self.get_sources():
            # if specified, make sure main config search path exists
            if source.provider == "main":
                if not source.available():
                    if source.scheme() == "pkg":
                        msg = (
                            f"Primary config module '{source.path}' not found."
                            f"\nCheck that it's correct and contains an __init__.py file"
                        )
                    else:
                        msg = (
                            f"Primary config directory not found."
                            f"\nCheck that the config directory '{source.path}' exists and readable"
                        )

                    self.missing_config_error(
                        config_name=None, msg=msg, with_search_path=False,
                    )

    def load_configuration(
        self,
        config_name: Optional[str],
        overrides: List[str],
        strict: Optional[bool] = None,
    ) -> DictConfig:
        if strict is None:
            strict = self.default_strict

        parsed_overrides = [self._parse_override(override) for override in overrides]

        if config_name is not None and not self.repository.config_exists(config_name):
            self.missing_config_error(
                config_name=config_name,
                msg=f"Cannot find primary config : {config_name}, check that it's in your config search path",
                with_search_path=True,
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

        config_group_overrides, config_overrides = self.split_overrides(
            parsed_overrides
        )
        self._combine_default_lists(defaults, job_defaults)
        ConfigLoaderImpl._apply_overrides_to_defaults(config_group_overrides, defaults)

        # Load and defaults and merge them into cfg
        cfg = self._merge_defaults_into_config(
            hydra_cfg, job_cfg, job_cfg_load_trace, defaults, split_at
        )
        OmegaConf.set_struct(cfg.hydra, True)
        OmegaConf.set_struct(cfg, strict)

        # Merge all command line overrides after enabling strict flag
        ConfigLoaderImpl._apply_overrides_to_config(
            [x.input_line for x in config_overrides], cfg
        )

        app_overrides = []
        for pwl in parsed_overrides:
            override = pwl.override
            assert override.key is not None
            key = override.key
            if key.startswith("hydra.") or key.startswith("hydra/"):
                cfg.hydra.overrides.hydra.append(pwl.input_line)
            else:
                cfg.hydra.overrides.task.append(pwl.input_line)
                app_overrides.append(pwl)

        with open_dict(cfg.hydra.job):
            if "name" not in cfg.hydra.job:
                cfg.hydra.job.name = JobRuntime().get("name")
            cfg.hydra.job.override_dirname = get_overrides_dirname(
                input_list=app_overrides,
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

    def get_search_path(self) -> ConfigSearchPath:
        return self.config_search_path

    def get_load_history(self) -> List[LoadTrace]:
        """
        returns the load history (which configs were attempted to load, and if they
        were loaded successfully or not.
        """
        return copy.deepcopy(self.all_config_checked)

    @staticmethod
    def is_matching(override: ParsedOverride, default: DefaultElement) -> bool:
        assert override.key == default.config_group
        if override.is_delete():
            return override.get_subject_package() == default.package
        else:
            return override.key == default.config_group and (
                override.pkg1 == default.package
                or override.pkg1 == ""
                and default.package is None
            )

    @staticmethod
    def find_matches(
        key_to_defaults: Dict[str, List[IndexedDefaultElement]],
        override: ParsedOverride,
    ) -> List[IndexedDefaultElement]:
        matches: List[IndexedDefaultElement] = []
        for default in key_to_defaults[override.key]:
            if ConfigLoaderImpl.is_matching(override, default.default):
                matches.append(default)
        return matches

    @staticmethod
    def _apply_overrides_to_defaults(
        overrides: List[ParsedOverrideWithLine], defaults: List[DefaultElement],
    ) -> None:

        key_to_defaults: Dict[str, List[IndexedDefaultElement]] = defaultdict(list)

        for idx, default in enumerate(defaults):
            if default.config_group is not None:
                key_to_defaults[default.config_group].append(
                    IndexedDefaultElement(idx=idx, default=default)
                )
        for owl in overrides:
            override = owl.override
            if override.value == "null":
                if override.prefix not in (None, "~"):
                    ConfigLoaderImpl._raise_parse_override_error(owl.input_line)
                override.prefix = "~"
                override.value = None

                msg = (
                    "\nRemoving from the defaults list by assigning 'null' "
                    "is deprecated and will be removed in Hydra 1.1."
                    f"\nUse ~{override.key}"
                )
                warnings.warn(category=UserWarning, message=msg)

            if (
                not (override.is_delete() or override.is_package_rename())
                and override.value is None
            ):
                ConfigLoaderImpl._raise_parse_override_error(owl.input_line)

            if override.is_add() and override.is_package_rename():
                raise HydraException(
                    "Add syntax does not support package rename, remove + prefix"
                )

            if override.value is not None and "," in override.value:
                # If this is a multirun config (comma separated list), flag the default to prevent it from being
                # loaded until we are constructing the config for individual jobs.
                override.value = "_SKIP_"

            matches = ConfigLoaderImpl.find_matches(key_to_defaults, override)

            if override.is_delete():
                src = override.get_source_item()
                if len(matches) == 0:
                    raise HydraException(
                        f"Could not delete. No match for '{src}' in the defaults list."
                    )
                for pair in matches:
                    if (
                        override.value is not None
                        and override.value != defaults[pair.idx].config_name
                    ):
                        raise HydraException(
                            f"Could not delete. No match for '{src}={override.value}' in the defaults list."
                        )

                    del defaults[pair.idx]
            elif override.is_add():
                if len(matches) > 0:
                    src = override.get_source_item()
                    raise HydraException(
                        f"Could not add. An item matching '{src}' is already in the defaults list."
                    )
                assert override.value is not None
                defaults.append(
                    DefaultElement(
                        config_group=override.key,
                        config_name=override.value,
                        package=override.get_subject_package(),
                    )
                )
            else:
                # override
                for match in matches:
                    default = match.default
                    if override.value is not None:
                        default.config_name = override.value
                    if override.pkg1 is not None:
                        default.package = override.get_subject_package()

                if len(matches) == 0:
                    src = override.get_source_item()
                    if override.is_package_rename():
                        msg = f"Could not rename package. No match for '{src}' in the defaults list."
                    else:
                        msg = (
                            f"Could not override '{src}'. No match in the defaults list."
                            f"\nTo append to your default list use +{owl.input_line}"
                        )

                    raise HydraException(msg)

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
    def _apply_overrides_to_config(overrides: List[str], cfg: DictConfig) -> None:
        loader = _utils.get_yaml_loader()

        def get_value(val_: Optional[str]) -> Any:
            return yaml.load(val_, Loader=loader) if val_ is not None else None

        for line in overrides:
            override = ConfigLoaderImpl._parse_config_override(line)
            try:
                value = get_value(override.value)
                if override.is_delete():
                    val = OmegaConf.select(cfg, override.key, throw_on_missing=False)
                    if val is None:
                        raise HydraException(
                            f"Could not delete from config. '{override.key}' does not exist."
                        )
                    elif value is not None and value != val:
                        raise HydraException(
                            f"Could not delete from config."
                            f" The value of '{override.key}' is {val} and not {override.value}."
                        )

                    key = override.key
                    last_dot = key.rfind(".")
                    with open_dict(cfg):
                        if last_dot == -1:
                            del cfg[key]
                        else:
                            node = OmegaConf.select(cfg, key[0:last_dot])
                            del node[key[last_dot + 1 :]]

                elif override.is_add():
                    if (
                        OmegaConf.select(cfg, override.key, throw_on_missing=False)
                        is None
                    ):
                        with open_dict(cfg):
                            OmegaConf.update(cfg, override.key, value)
                    else:
                        raise HydraException(
                            f"Could not append to config. An item is already at '{override.key}'."
                        )
                else:
                    try:
                        OmegaConf.update(cfg, override.key, value)
                    except (ConfigAttributeError, ConfigKeyError) as ex:
                        raise HydraException(
                            f"Could not override '{override.key}'. No match in config."
                            f"\nTo append to your config use +{line}"
                        ) from ex
            except OmegaConfBaseException as ex:
                raise HydraException(f"Error merging override {line}") from ex

    @staticmethod
    def _raise_parse_override_error(override: str) -> str:
        msg = (
            f"Error parsing config group override : '{override}'"
            f"\nAccepted forms:"
            f"\n\tOverride: key=value, key@package=value, key@src_pkg:dest_pkg=value, key@src_pkg:dest_pkg"
            f"\n\tAppend:  +key=value, +key@package=value"
            f"\n\tDelete:  ~key, ~key@pkg, ~key=value, ~key@pkg=value"
        )
        raise HydraException(msg)

    @staticmethod
    def _parse_override(override: str) -> ParsedOverrideWithLine:
        # forms:
        # key=value
        # key@pkg=value
        # key@src_pkg:dst_pkg=value
        # regex code and tests: https://regex101.com/r/LiV6Rf/14

        regex = (
            r"^(?P<prefix>[+~])?(?P<key>[A-Za-z0-9_.-/]+)(?:@(?P<pkg1>[A-Za-z0-9_\.-]*)"
            r"(?::(?P<pkg2>[A-Za-z0-9_\.-]*)?)?)?(?:=(?P<value>.*))?$"
        )
        matches = re.search(regex, override)
        if matches:
            prefix = matches.group("prefix")
            key = matches.group("key")
            pkg1 = matches.group("pkg1")
            pkg2 = matches.group("pkg2")
            value: Optional[str] = matches.group("value")
            ret = ParsedOverride(prefix, key, pkg1, pkg2, value)
            return ParsedOverrideWithLine(override=ret, input_line=override)
        else:
            ConfigLoaderImpl._raise_parse_override_error(override)
            assert False

    @staticmethod
    def _parse_config_override(override: str) -> ParsedConfigOverride:
        # forms:
        # update: key=value
        # append: +key=value
        # delete: ~key=value | ~key
        # regex code and tests: https://regex101.com/r/JAPVdx/9

        regex = r"^(?P<prefix>[+~])?(?P<key>[\w\.@]+)(?:=(?P<value>.*))?$"
        matches = re.search(regex, override)

        valid = True
        prefix = None
        key = None
        value = None
        msg = (
            f"Error parsing config override : '{override}'"
            f"\nAccepted forms:"
            f"\n\tOverride:  key=value"
            f"\n\tAppend:   +key=value"
            f"\n\tDelete:   ~key=value, ~key"
        )
        if matches:
            prefix = matches.group("prefix")
            key = matches.group("key")
            value = matches.group("value")
            if prefix in (None, "+"):
                valid = key is not None and value is not None
            elif prefix == "~":
                valid = key is not None

        if matches and valid:
            assert key is not None
            return ParsedConfigOverride(prefix=prefix, key=key, value=value)
        else:
            raise HydraException(msg)

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


def get_overrides_dirname(
    input_list: List[ParsedOverrideWithLine],
    exclude_keys: List[str] = [],
    item_sep: str = ",",
    kv_sep: str = "=",
) -> str:
    lines = []
    for x in input_list:
        if x.override.key not in exclude_keys:
            lines.append(x.input_line)

    lines.sort()
    ret = re.sub(pattern="[=]", repl=kv_sep, string=item_sep.join(lines))
    return ret
