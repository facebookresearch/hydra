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

    def load_config(self, config_path: str) -> Optional[ConfigResult]:
        source = self._find_config(config_path=config_path)
        ret = None
        if source is not None:
            ret = source.load_config(config_path=config_path)
            # if this source is THE schema source, flag the result as coming from it.
            ret.is_schema_source = (
                source.__class__.__name__ == "StructuredConfigSource"
                and source.provider == "schema"
            )
        return ret

    def exists(self, config_path: str) -> bool:
        return self._find_config(config_path) is not None

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

    def _find_config(self, config_path: str) -> Optional[ConfigSource]:
        found_source = None
        for source in self.sources:
            if source.exists(config_path):
                found_source = source
                break
        return found_source

    @staticmethod
    def _get_scheme(path: str) -> str:
        idx = path.find("://")
        if idx == -1:
            return "file"
        else:
            return path[0:idx]
