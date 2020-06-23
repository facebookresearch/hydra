# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigResult, ConfigSource

from .sources_registry import SourcesRegistry


class ConfigRepository:

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

    def load_config(
        self,
        config_path: str,
        is_primary_config: bool,
        package_override: Optional[str] = None,
    ) -> Optional[ConfigResult]:
        source = self._find_object_source(
            config_path=config_path, object_type=ObjectType.CONFIG
        )
        ret = None
        if source is not None:
            ret = source.load_config(
                config_path=config_path,
                is_primary_config=is_primary_config,
                package_override=package_override,
            )
            # if this source is THE schema source, flag the result as coming from it.
            ret.is_schema_source = (
                source.__class__.__name__ == "StructuredConfigSource"
                and source.provider == "schema"
            )
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
