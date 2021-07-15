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
from textwrap import dedent
from typing import Any, Dict, List, Optional, Tuple

from omegaconf import Container, DictConfig, ListConfig, OmegaConf, open_dict
from omegaconf.errors import (
    ConfigAttributeError,
    ConfigKeyError,
    OmegaConfBaseException,
)

from hydra._internal.config_repository import ConfigRepository
from hydra.core.config_loader import ConfigLoader, LoadTrace
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.object_type import ObjectType
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import Override, OverrideType, ValueType
from hydra.core.utils import JobRuntime
from hydra.errors import ConfigCompositionException, MissingConfigException
from hydra.plugins.config_source import ConfigLoadError, ConfigSource
from hydra.types import RunMode


class UnspecifiedMandatoryDefault(Exception):
    def __init__(self, config_group: str) -> None:
        self.config_group = config_group


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
        default_strict: Optional[bool] = True,
    ) -> None:
        self.default_strict = default_strict
        self.all_config_checked: List[LoadTrace] = []
        self.config_search_path = config_search_path
        self.repository: ConfigRepository = ConfigRepository(
            config_search_path=config_search_path
        )

    def split_by_override_type(
        self, overrides: List[Override]
    ) -> Tuple[List[Override], List[Override]]:
        config_group_overrides = []
        config_overrides = []
        for override in overrides:
            is_group = self.repository.group_exists(override.key_or_group)
            is_dict = isinstance(override.value(), dict)
            if is_dict or not is_group:
                config_overrides.append(override)
            else:
                config_group_overrides.append(override)
        return config_group_overrides, config_overrides

    def missing_config_error(
        self, config_name: Optional[str], msg: str, with_search_path: bool
    ) -> None:
        def add_search_path() -> str:
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
            missing_cfg_file=config_name, message=add_search_path()
        )

    def ensure_main_config_source_available(self) -> None:
        for source in self.get_sources():
            # if specified, make sure main config search path exists
            if source.provider == "main":
                if not source.available():
                    if source.scheme() == "pkg":
                        if source.path == "":
                            msg = (
                                "Primary config module is empty."
                                "\nPython requires resources to be in a module with an __init__.py file"
                            )
                        else:
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
                        config_name=None, msg=msg, with_search_path=False
                    )

    def load_configuration(
        self,
        config_name: Optional[str],
        overrides: List[str],
        run_mode: RunMode,
        strict: Optional[bool] = None,
        from_shell: bool = True,
    ) -> DictConfig:
        try:
            return self._load_configuration(
                config_name=config_name,
                overrides=overrides,
                run_mode=run_mode,
                strict=strict,
                from_shell=from_shell,
            )
        except OmegaConfBaseException as e:
            raise ConfigCompositionException() from e

    def _load_configuration(
        self,
        config_name: Optional[str],
        overrides: List[str],
        run_mode: RunMode,
        strict: Optional[bool] = None,
        from_shell: bool = True,
    ) -> DictConfig:
        if config_name is not None and not self.repository.config_exists(config_name):
            self.missing_config_error(
                config_name=config_name,
                msg=f"Cannot find primary config : {config_name}, check that it's in your config search path",
                with_search_path=True,
            )

        if strict is None:
            strict = self.default_strict

        parser = OverridesParser.create()
        parsed_overrides = parser.parse_overrides(overrides=overrides)
        config_overrides = []
        sweep_overrides = []
        for x in parsed_overrides:
            if x.is_sweep_override():
                if run_mode == RunMode.MULTIRUN:
                    if x.is_hydra_override():
                        raise ConfigCompositionException(
                            f"Sweeping over Hydra's configuration is not supported : '{x.input_line}'"
                        )
                    sweep_overrides.append(x)
                elif run_mode == RunMode.RUN:
                    if x.value_type == ValueType.SIMPLE_CHOICE_SWEEP:
                        vals = "value1,value2"
                        if from_shell:
                            example_override = f"key=\\'{vals}\\'"
                        else:
                            example_override = f"key='{vals}'"

                        msg = dedent(
                            f"""\
                            Ambiguous value for argument '{x.input_line}'
                            1. To use it as a list, use key=[value1,value2]
                            2. To use it as string, quote the value: {example_override}
                            3. To sweep over it, add --multirun to your command line"""
                        )
                        raise ConfigCompositionException(msg)
                    else:
                        raise ConfigCompositionException(
                            f"Sweep parameters '{x.input_line}' requires --multirun"
                        )
                else:
                    assert False
            else:
                config_overrides.append(x)

        config_group_overrides, config_overrides = self.split_by_override_type(
            config_overrides
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

            # during the regular merge later the config will retain the readonly flag.
            _recursive_unset_readonly(hydra_cfg)
            # this is breaking encapsulation a bit. can potentially be implemented in OmegaConf
            hydra_cfg._metadata.ref_type = job_cfg._metadata.ref_type

            OmegaConf.set_readonly(hydra_cfg.hydra, False)

        # if defaults are re-introduced by the promotion, remove it.
        if "defaults" in hydra_cfg:
            with open_dict(hydra_cfg):
                del hydra_cfg["defaults"]

        if config_name is not None:
            defaults.append(DefaultElement(config_group=None, config_name="__SELF__"))
        split_at = len(defaults)

        self._combine_default_lists(defaults, job_defaults)
        ConfigLoaderImpl._apply_overrides_to_defaults(config_group_overrides, defaults)

        # Load and defaults and merge them into cfg
        try:
            cfg = self._merge_defaults_into_config(
                hydra_cfg,
                job_cfg,
                job_cfg_load_trace,
                defaults,
                split_at,
                run_mode=run_mode,
            )
        except UnspecifiedMandatoryDefault as e:
            options = self.get_group_options(e.config_group)
            opt_list = "\n".join(["\t" + x for x in options])
            msg = (
                f"You must specify '{e.config_group}', e.g, {e.config_group}=<OPTION>"
                f"\nAvailable options:"
                f"\n{opt_list}"
            )
            raise ConfigCompositionException(msg) from e

        OmegaConf.set_struct(cfg, strict)

        # Apply command line overrides after enabling strict flag
        ConfigLoaderImpl._apply_overrides_to_config(config_overrides, cfg)

        app_overrides = []
        for override in parsed_overrides:
            if override.is_hydra_override():
                cfg.hydra.overrides.hydra.append(override.input_line)
            else:
                cfg.hydra.overrides.task.append(override.input_line)
                app_overrides.append(override)

        with open_dict(cfg.hydra.job):
            if "name" not in cfg.hydra.job:
                cfg.hydra.job.name = JobRuntime().get("name")
            cfg.hydra.job.override_dirname = get_overrides_dirname(
                overrides=app_overrides,
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
            run_mode=RunMode.RUN,
        )

        with open_dict(sweep_config):
            sweep_config.hydra.runtime.merge_with(master_config.hydra.runtime)

        # Partial copy of master config cache, to ensure we get the same resolved values for timestamps
        cache: Dict[str, Any] = defaultdict(dict, {})
        cache_master_config = OmegaConf.get_cache(master_config)
        for k in ["now"]:
            if k in cache_master_config:
                cache[k] = cache_master_config[k]
        OmegaConf.set_cache(sweep_config, cache)

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
    def is_matching(override: Override, default: DefaultElement) -> bool:
        assert override.key_or_group == default.config_group
        if override.is_delete():
            return override.get_subject_package() == default.package
        else:
            return override.key_or_group == default.config_group and (
                override.pkg1 == default.package
                or override.pkg1 == ""
                and default.package is None
            )

    @staticmethod
    def find_matches(
        key_to_defaults: Dict[str, List[IndexedDefaultElement]], override: Override
    ) -> List[IndexedDefaultElement]:
        matches: List[IndexedDefaultElement] = []
        for default in key_to_defaults[override.key_or_group]:
            if ConfigLoaderImpl.is_matching(override, default.default):
                matches.append(default)
        return matches

    @staticmethod
    def _apply_overrides_to_defaults(
        overrides: List[Override], defaults: List[DefaultElement]
    ) -> None:

        key_to_defaults: Dict[str, List[IndexedDefaultElement]] = defaultdict(list)

        for idx, default in enumerate(defaults):
            if default.config_group is not None:
                key_to_defaults[default.config_group].append(
                    IndexedDefaultElement(idx=idx, default=default)
                )
        for override in overrides:
            value = override.value()
            if value is None:
                if override.is_add():
                    ConfigLoaderImpl._raise_parse_override_error(override.input_line)

                if not override.is_delete():
                    override.type = OverrideType.DEL
                    msg = (
                        "\nRemoving from the defaults list by assigning 'null' "
                        "is deprecated and will be removed in Hydra 1.1."
                        f"\nUse ~{override.key_or_group}"
                    )
                    warnings.warn(category=UserWarning, message=msg)
            if (
                not (override.is_delete() or override.is_package_rename())
                and value is None
            ):
                ConfigLoaderImpl._raise_parse_override_error(override.input_line)

            if override.is_add() and override.is_package_rename():
                raise ConfigCompositionException(
                    "Add syntax does not support package rename, remove + prefix"
                )

            matches = ConfigLoaderImpl.find_matches(key_to_defaults, override)

            if isinstance(value, (list, dict)):
                raise ConfigCompositionException(
                    f"Config group override value type cannot be a {type(value).__name__}"
                )

            if override.is_delete():
                src = override.get_source_item()
                if len(matches) == 0:
                    raise ConfigCompositionException(
                        f"Could not delete. No match for '{src}' in the defaults list."
                    )
                for pair in matches:
                    if value is not None and value != defaults[pair.idx].config_name:
                        raise ConfigCompositionException(
                            f"Could not delete. No match for '{src}={value}' in the defaults list."
                        )

                    del defaults[pair.idx]
            elif override.is_add():
                if len(matches) > 0:
                    src = override.get_source_item()
                    raise ConfigCompositionException(
                        f"Could not add '{src}={override.get_value_string()}'."
                        f" '{src}' is already in the defaults list."
                    )
                assert value is not None
                defaults.append(
                    DefaultElement(
                        config_group=override.key_or_group,
                        config_name=str(value),
                        package=override.get_subject_package(),
                    )
                )
            else:
                assert value is not None
                # override
                for match in matches:
                    default = match.default
                    default.config_name = str(value)
                    if override.is_package_rename():
                        default.package = override.get_subject_package()

                if len(matches) == 0:
                    src = override.get_source_item()
                    if override.is_package_rename():
                        msg = f"Could not rename package. No match for '{src}' in the defaults list."
                    else:
                        msg = (
                            f"Could not override '{src}'. No match in the defaults list."
                            f"\nTo append to your default list use +{override.input_line}"
                        )

                    raise ConfigCompositionException(msg)

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
    def _apply_overrides_to_config(overrides: List[Override], cfg: DictConfig) -> None:
        for override in overrides:
            if override.get_subject_package() is not None:
                raise ConfigCompositionException(
                    f"Override {override.input_line} looks like a config group override, "
                    f"but config group '{override.key_or_group}' does not exist."
                )

            key = override.key_or_group
            value = override.value()
            try:
                if override.is_delete():
                    config_val = OmegaConf.select(cfg, key, throw_on_missing=False)
                    if config_val is None:
                        raise ConfigCompositionException(
                            f"Could not delete from config. '{override.key_or_group}' does not exist."
                        )
                    elif value is not None and value != config_val:
                        raise ConfigCompositionException(
                            f"Could not delete from config."
                            f" The value of '{override.key_or_group}' is {config_val} and not {value}."
                        )

                    last_dot = key.rfind(".")
                    with open_dict(cfg):
                        if last_dot == -1:
                            del cfg[key]
                        else:
                            node = OmegaConf.select(cfg, key[0:last_dot])
                            del node[key[last_dot + 1 :]]

                elif override.is_add():
                    if OmegaConf.select(
                        cfg, key, throw_on_missing=False
                    ) is None or isinstance(value, (dict, list)):
                        with open_dict(cfg):
                            OmegaConf.update(cfg, key, value, merge=True)
                    else:
                        raise ConfigCompositionException(
                            f"Could not append to config. An item is already at '{override.key_or_group}'."
                        )
                else:
                    try:
                        OmegaConf.update(cfg, key, value, merge=True)
                    except (ConfigAttributeError, ConfigKeyError) as ex:
                        raise ConfigCompositionException(
                            f"Could not override '{override.key_or_group}'."
                            f"\nTo append to your config use +{override.input_line}"
                        ) from ex
            except OmegaConfBaseException as ex:
                raise ConfigCompositionException(
                    f"Error merging override {override.input_line}"
                ) from ex

    @staticmethod
    def _raise_parse_override_error(override: Optional[str]) -> None:
        msg = (
            f"Error parsing config group override : '{override}'"
            f"\nAccepted forms:"
            f"\n\tOverride: key=value, key@package=value, key@src_pkg:dest_pkg=value, key@src_pkg:dest_pkg"
            f"\n\tAppend:  +key=value, +key@package=value"
            f"\n\tDelete:  ~key, ~key@pkg, ~key=value, ~key@pkg=value"
            f"\n"
            f"\nSee https://hydra.cc/docs/next/advanced/override_grammar/basic for details"
        )
        raise ConfigCompositionException(msg)

    def _record_loading(
        self,
        name: str,
        path: Optional[str],
        provider: Optional[str],
        schema_provider: Optional[str],
        record_load: bool,
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

                    try:
                        if is_primary_config:
                            # Add as placeholders for hydra and defaults to allow
                            # overriding them from the config even if not in schema
                            schema.config = OmegaConf.merge(
                                {"hydra": None, "defaults": []}, schema.config
                            )

                        merged = OmegaConf.merge(schema.config, ret.config)
                        assert isinstance(merged, DictConfig)

                        # remove placeholders if unused
                        with open_dict(merged):
                            if "hydra" in merged and merged.hydra is None:
                                del merged["hydra"]
                            if "defaults" in merged and merged["defaults"] == []:
                                del merged["defaults"]
                    except OmegaConfBaseException as e:
                        raise ConfigCompositionException(
                            f"Error merging '{input_file}' with schema"
                        ) from e

                    assert isinstance(merged, DictConfig)
                    return (
                        merged,
                        self._record_loading(
                            name=input_file,
                            path=ret.path,
                            provider=ret.provider,
                            schema_provider=schema.provider,
                            record_load=record_load,
                        ),
                    )

                except ConfigLoadError:
                    # schema not found, ignore
                    pass

            return (
                ret.config,
                self._record_loading(
                    name=input_file,
                    path=ret.path,
                    provider=ret.provider,
                    schema_provider=None,
                    record_load=record_load,
                ),
            )
        else:
            return (
                None,
                self._record_loading(
                    name=input_file,
                    path=None,
                    provider=None,
                    schema_provider=None,
                    record_load=record_load,
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
                            opt_list = "\n".join(["\t" + x for x in options])
                            msg = (
                                f"Could not load {new_cfg}.\nAvailable options:"
                                f"\n{opt_list}"
                            )
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
            raise ConfigCompositionException(
                f"Error merging {config_group}={name}"
            ) from ex

    def _merge_defaults_into_config(
        self,
        hydra_cfg: DictConfig,
        job_cfg: DictConfig,
        job_cfg_load_trace: Optional[LoadTrace],
        defaults: List[DefaultElement],
        split_at: int,
        run_mode: RunMode,
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
                    if OmegaConf.is_missing(
                        dict_with_list.defaults[idx], default1.config_group
                    ):
                        if run_mode == RunMode.RUN:
                            raise UnspecifiedMandatoryDefault(
                                config_group=default1.config_group
                            )
                        else:
                            config_name = "???"
                    else:
                        config_name = dict_with_list.defaults[idx][
                            default1.config_group
                        ]
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
                    if default1.config_name not in (None, "_SKIP_", "???", "_self_"):
                        merged_cfg = self._merge_config(
                            cfg=merged_cfg,
                            config_group=default1.config_group,
                            name=config_name,
                            required=not default1.optional,
                            is_primary_config=False,
                            package_override=default1.package,
                        )
                else:
                    if default1.config_name not in ("_SKIP_", "_self_"):
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
    overrides: List[Override], exclude_keys: List[str], item_sep: str, kv_sep: str
) -> str:
    lines = []
    for override in overrides:
        if override.key_or_group not in exclude_keys:
            line = override.input_line
            assert line is not None
            lines.append(line)

    lines.sort()
    ret = re.sub(pattern="[=]", repl=kv_sep, string=item_sep.join(lines))
    return ret


def _recursive_unset_readonly(cfg: Container) -> None:
    if isinstance(cfg, DictConfig):
        OmegaConf.set_readonly(cfg, None)
        if not (cfg._is_missing() or cfg._is_none()):
            for k, v in cfg.items_ex(resolve=False):
                _recursive_unset_readonly(v)
    elif isinstance(cfg, ListConfig):
        OmegaConf.set_readonly(cfg, None)
        if not (cfg._is_missing() or cfg._is_none()):
            for item in cfg:
                _recursive_unset_readonly(item)
