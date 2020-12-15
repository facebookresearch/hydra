# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, List, Optional, Tuple

from omegaconf import (
    Container,
    DictConfig,
    ListConfig,
    OmegaConf,
    open_dict,
    read_write,
)

from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigResult, ConfigSource

from ..core.default_element import ConfigDefault, GroupDefault, InputDefault
from .sources_registry import SourcesRegistry


class IConfigRepository(ABC):
    @abstractmethod
    def get_schema_source(self) -> ConfigSource:
        ...

    @abstractmethod
    def load_config(self, config_path: str) -> Optional[ConfigResult]:
        ...

    @abstractmethod
    def group_exists(self, config_path: str) -> bool:
        ...

    @abstractmethod
    def config_exists(self, config_path: str) -> bool:
        ...

    @abstractmethod
    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        ...

    @abstractmethod
    def get_sources(self) -> List[ConfigSource]:
        ...


class ConfigRepository(IConfigRepository):

    config_search_path: ConfigSearchPath
    sources: List[ConfigSource]

    def __init__(self, config_search_path: ConfigSearchPath) -> None:
        self.sources = []
        for search_path in config_search_path.get_path():
            assert search_path.path is not None
            assert search_path.provider is not None
            scheme = self._get_scheme(search_path.path)
            source_type = SourcesRegistry.instance().resolve(scheme)
            source = source_type(search_path.provider, search_path.path)
            self.sources.append(source)

    def get_schema_source(self) -> ConfigSource:
        source = self.sources[-1]  # should always be last
        assert (
            source.__class__.__name__ == "StructuredConfigSource"
            and source.provider == "schema"
        )
        return source

    def load_config(self, config_path: str) -> Optional[ConfigResult]:
        source = self._find_object_source(
            config_path=config_path, object_type=ObjectType.CONFIG
        )
        ret = None
        if source is not None:
            ret = source.load_config(config_path=config_path)
            # if this source is THE schema source, flag the result as coming from it.
            ret.is_schema_source = (
                source.__class__.__name__ == "StructuredConfigSource"
                and source.provider == "schema"
            )

        if ret is not None:
            raw_defaults = self._extract_defaults_list(config_path, ret.config)
            ret.defaults_list = self._create_defaults_list(config_path, raw_defaults)

            # # TODO: push to a higher level?
            # ret = self._embed_result_config(ret, package_override)

        return ret

    def group_exists(self, config_path: str) -> bool:
        return self._find_object_source(config_path, ObjectType.GROUP) is not None

    def config_exists(self, config_path: str) -> bool:
        return self._find_object_source(config_path, ObjectType.CONFIG) is not None

    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        options: List[str] = []
        for source in self.sources:
            if source.is_group(config_path=group_name):
                options.extend(
                    source.list(config_path=group_name, results_filter=results_filter)
                )
        return sorted(list(set(options)))

    def get_sources(self) -> List[ConfigSource]:
        return self.sources

    def _find_object_source(
        self, config_path: str, object_type: Optional[ObjectType]
    ) -> Optional[ConfigSource]:
        found_source = None
        for source in self.sources:
            if object_type == ObjectType.CONFIG:
                if source.is_config(config_path):
                    found_source = source
                    break
            elif object_type == ObjectType.GROUP:
                if source.is_group(config_path):
                    found_source = source
                    break
            else:
                raise ValueError("Unexpected object_type")
        return found_source

    @staticmethod
    def _get_scheme(path: str) -> str:
        idx = path.find("://")
        if idx == -1:
            return "file"
        else:
            return path[0:idx]

    def _split_group(
        self,
        group_with_package: str,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        idx = group_with_package.find("@")
        if idx == -1:
            # group
            group = group_with_package
            package = None
        else:
            # group@package
            group = group_with_package[0:idx]
            package = group_with_package[idx + 1 :]

        package2 = None
        if package is not None:
            # if we have a package, break it down if it's a rename
            idx = package.find(":")
            if idx != -1:
                package2 = package[idx + 1 :]
                package = package[0:idx]

        return group, package, package2

    def _create_defaults_list(
        self,
        config_path: str,
        defaults: ListConfig,
    ) -> List[InputDefault]:
        res: List[InputDefault] = []
        for item in defaults:
            default: InputDefault
            if isinstance(item, DictConfig):

                old_optional = None
                if "optional" in item:
                    old_optional = item.pop("optional")
                keys = list(item.keys())

                if len(keys) > 1:
                    raise ValueError(
                        f"In {config_path}: Too many keys in default item {item}"
                    )
                if len(keys) == 0:
                    raise ValueError(f"In {config_path}: Missing group name in {item}")

                key = keys[0]
                config_group, package, _package2 = self._split_group(key)
                keywords = ConfigRepository.Keywords()
                self._extract_keywords_from_config_group(config_group, keywords)

                if not keywords.optional and old_optional is not None:
                    keywords.optional = old_optional

                node = item._get_node(key)
                assert node is not None
                config_name = node._value()

                if old_optional is not None:
                    # DEPRECATED: remove in 1.2
                    msg = dedent(
                        f"""
                        In {config_path}: 'optional: true' is deprecated.
                        Use 'optional {key}: {config_name}' instead.
                        Support for the old style will be removed in a future version of Hydra"""
                    )

                    warnings.warn(msg)

                default = GroupDefault(
                    group=keywords.group,
                    name=config_name,
                    package=package,
                    optional=keywords.optional,
                    override=keywords.override,
                )
            elif isinstance(item, str):
                path, package, _package2 = self._split_group(item)
                default = ConfigDefault(path=path, package=package)
            else:
                raise ValueError(
                    f"Unsupported type in defaults : {type(item).__name__}"
                )
            res.append(default)
        return res

    def _extract_defaults_list(self, config_path: str, cfg: Container) -> ListConfig:
        empty = OmegaConf.create([])
        if not OmegaConf.is_dict(cfg):
            return empty
        assert isinstance(cfg, DictConfig)
        with read_write(cfg):
            with open_dict(cfg):
                defaults = cfg.pop("defaults", empty)
        if not isinstance(defaults, ListConfig):
            raise ValueError(
                dedent(
                    f"""\
                    Invalid defaults list in '{config_path}', defaults must be a list.
                    Example of a valid defaults:
                    defaults:
                      - dataset: imagenet
                      - override hydra/launcher: fancy_launcher
                    """
                )
            )

        return defaults

    @dataclass
    class Keywords:
        optional: bool = False
        override: bool = False
        group: str = ""

    @staticmethod
    def _extract_keywords_from_config_group(
        group: str, keywords: "ConfigRepository.Keywords"
    ) -> None:
        elements = group.split(" ")
        for idx, e in enumerate(elements):
            if e == "optional":
                keywords.optional = True
            elif e == "override":
                keywords.override = True
            else:
                break
        keywords.group = " ".join(elements[idx:])


class CachingConfigRepository(IConfigRepository):
    def __init__(self, delegeate: IConfigRepository):
        self.delegate = delegeate
        self.cache: Dict[str, Optional[ConfigResult]] = {}

    def get_schema_source(self) -> ConfigSource:
        return self.delegate.get_schema_source()

    def load_config(self, config_path: str) -> Optional[ConfigResult]:
        cache_key = f"config_path={config_path}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        else:
            ret = self.delegate.load_config(config_path=config_path)
            self.cache[cache_key] = ret
            return ret

    def group_exists(self, config_path: str) -> bool:
        return self.delegate.group_exists(config_path=config_path)

    def config_exists(self, config_path: str) -> bool:
        return self.delegate.config_exists(config_path=config_path)

    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        return self.delegate.get_group_options(
            group_name=group_name, results_filter=results_filter
        )

    def get_sources(self) -> List[ConfigSource]:
        return self.delegate.get_sources()
