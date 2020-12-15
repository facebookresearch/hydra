# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Configuration loader
"""
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Dict, List, Optional, Tuple

from omegaconf import DictConfig, OmegaConf, open_dict
from omegaconf.errors import (
    ConfigAttributeError,
    ConfigKeyError,
    OmegaConfBaseException,
)

from hydra._internal.config_repository import (
    CachingConfigRepository,
    ConfigRepository,
    IConfigRepository,
)
from hydra._internal.defaults_list import DefaultsList, create_defaults_list
from hydra.core.config_loader import ConfigLoader, LoadTrace
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.default_element import ResultDefault
from hydra.core.object_type import ObjectType
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import Override, ValueType
from hydra.core.utils import JobRuntime
from hydra.errors import ConfigCompositionException, MissingConfigException
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource
from hydra.types import RunMode


@dataclass
class SplitOverrides:
    config_group_overrides: List[Override]
    config_overrides: List[Override]


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
        self.config_search_path = config_search_path
        self.repository: ConfigRepository = ConfigRepository(
            config_search_path=config_search_path
        )

    @staticmethod
    def parse_overrides(
        overrides: List[str],
        run_mode: RunMode,
        from_shell: bool,
    ) -> List[Override]:
        parser = OverridesParser.create()
        parsed_overrides = parser.parse_overrides(overrides=overrides)
        config_overrides = []
        for x in parsed_overrides:
            if x.is_sweep_override():
                if run_mode == RunMode.MULTIRUN:
                    if x.is_hydra_override():
                        raise ConfigCompositionException(
                            f"Sweeping over Hydra's configuration is not supported : '{x.input_line}'"
                        )
                    # do not process sweep overrides in multirun mode.
                    # They will be handled directly by the sweeper
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
        return config_overrides

    def split_by_override_type(self, overrides: List[Override]) -> SplitOverrides:
        config_group_overrides = []
        config_overrides = []
        for override in overrides:
            is_group = self.repository.group_exists(override.key_or_group)
            is_dict = isinstance(override.value(), dict)
            if is_dict or not is_group:
                config_overrides.append(override)
            else:
                config_group_overrides.append(override)
        return SplitOverrides(
            config_group_overrides=config_group_overrides,
            config_overrides=config_overrides,
        )

    def _missing_config_error(
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

                    self._missing_config_error(
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
            cfg = self._load_configuration_impl(
                config_name=config_name,
                overrides=overrides,
                run_mode=run_mode,
                strict=strict,
                from_shell=from_shell,
            )
            return cfg
        except OmegaConfBaseException as e:
            raise ConfigCompositionException().with_traceback(sys.exc_info()[2]) from e

    def _load_configuration_impl(
        self,
        config_name: Optional[str],
        overrides: List[str],
        run_mode: RunMode,
        strict: Optional[bool] = None,
        from_shell: bool = True,
    ) -> DictConfig:
        self.ensure_main_config_source_available()
        caching_repo = CachingConfigRepository(self.repository)

        if config_name is not None and not caching_repo.config_exists(config_name):
            self._missing_config_error(
                config_name=config_name,
                msg=f"Cannot find primary config : {config_name}, check that it's in your config search path",
                with_search_path=True,
            )

        if strict is None:
            strict = self.default_strict

        parser = OverridesParser.create()
        parsed_overrides = parser.parse_overrides(overrides=overrides)

        # TODO: decide where the error checking in this function should be.
        #  This function can parse and validate the overrides without splitting them into types
        config_overrides = ConfigLoaderImpl.parse_overrides(
            overrides=overrides, run_mode=run_mode, from_shell=from_shell
        )

        defaults_list = create_defaults_list(
            repo=caching_repo,
            config_name=config_name,
            overrides_list=parser.parse_overrides(overrides=overrides),
            prepend_hydra=True,
            skip_missing=run_mode == RunMode.MULTIRUN,
        )

        config_overrides = defaults_list.config_overrides

        cfg, composition_trace = self._compose_config_from_defaults_list(
            primary_config_name=config_name,
            defaults=defaults_list.defaults,
            repo=caching_repo,
        )

        OmegaConf.set_struct(cfg, strict)
        OmegaConf.set_readonly(cfg.hydra, False)

        # Apply command line overrides after enabling strict flag
        ConfigLoaderImpl._apply_overrides_to_config(config_overrides, cfg)
        app_overrides = []
        for override in parsed_overrides:
            if override.is_hydra_override():
                cfg.hydra.overrides.hydra.append(override.input_line)
            else:
                cfg.hydra.overrides.task.append(override.input_line)
                app_overrides.append(override)

        with open_dict(cfg.hydra):
            from hydra import __version__

            cfg.hydra.runtime.version = __version__
            cfg.hydra.runtime.cwd = os.getcwd()

            cfg.hydra.composition_trace = composition_trace
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

    @staticmethod
    def _apply_overrides_to_config(overrides: List[Override], cfg: DictConfig) -> None:
        for override in overrides:
            if override.package is not None:
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

    def _load_single_config(
        self, default: ResultDefault, repo: IConfigRepository, is_primary: bool
    ) -> Tuple[ConfigResult, LoadTrace]:
        config_path = default.config_path
        package = default.package

        assert config_path is not None
        ret = repo.load_config(config_path=config_path, package_override=package)
        assert ret is not None

        if not isinstance(ret.config, DictConfig):
            raise ValueError(
                f"Config {config_path} must be a Dictionary, got {type(ret).__name__}"
            )

        if not ret.is_schema_source:
            schema = None
            try:
                schema_source = repo.get_schema_source()
                cname = ConfigSource._normalize_file_name(filename=config_path)
                schema = schema_source.load_config(cname)
            except ConfigLoadError:
                # schema not found, ignore
                pass

            if schema is not None:
                try:
                    # if config has a hydra node, remove it during validation and add it back.
                    # This allows overriding Hydra's configuration without declaring this node
                    # in every program
                    hydra = None
                    hydra_config_group = (
                        default.config_path is not None
                        and default.config_path.startswith("hydra/")
                    )
                    if "hydra" in ret.config and not hydra_config_group:
                        hydra = ret.config.pop("hydra")

                    schema = repo._embed_result_config(schema, package)
                    merged = OmegaConf.merge(schema.config, ret.config)
                    assert isinstance(merged, DictConfig)

                    if hydra is not None:
                        with open_dict(merged):
                            merged.hydra = hydra
                    ret.config = merged
                except OmegaConfBaseException as e:
                    raise ConfigCompositionException(
                        f"Error merging '{config_path}' with schema"
                    ) from e

                assert isinstance(merged, DictConfig)

        trace = LoadTrace(
            config_path=default.config_path,
            package=default.package,
            parent=default.parent,
            is_self=default.is_self,
            search_path=ret.path,
            provider=ret.provider,
        )
        return ret, trace

    def list_groups(self, parent_name: str) -> List[str]:
        return self.get_group_options(
            group_name=parent_name, results_filter=ObjectType.GROUP
        )

    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        return self.repository.get_group_options(group_name, results_filter)

    def _compose_config_from_defaults_list(
        self,
        primary_config_name: Optional[str],
        defaults: List[ResultDefault],
        repo: IConfigRepository,
    ) -> Tuple[DictConfig, List[LoadTrace]]:
        composition_trace = []
        cfg = OmegaConf.create()
        for default in defaults:
            # TODO: if primary is critical return it in ResultDefault
            primary = default.config_path == primary_config_name

            loaded, trace = self._load_single_config(
                default=default, repo=repo, is_primary=primary
            )
            merged = OmegaConf.merge(cfg, loaded.config)
            assert isinstance(merged, DictConfig)
            cfg = merged
            assert cfg is not None
            composition_trace.append(trace)

        # This is primarily cosmetic
        cfg._metadata.ref_type = cfg._metadata.object_type

        return cfg, composition_trace

    def get_sources(self) -> List[ConfigSource]:
        return self.repository.get_sources()

    def compute_defaults_list(
        self,
        config_name: Optional[str],
        overrides: List[str],
        run_mode: RunMode,
    ) -> DefaultsList:
        parser = OverridesParser.create()
        repo = CachingConfigRepository(self.repository)
        defaults_list = create_defaults_list(
            repo=repo,
            config_name=config_name,
            overrides_list=parser.parse_overrides(overrides=overrides),
            prepend_hydra=True,
            skip_missing=run_mode == RunMode.MULTIRUN,
        )
        return defaults_list


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
