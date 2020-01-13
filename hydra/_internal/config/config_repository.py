# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from hydra._internal.config_search_path import ConfigSearchPath
from hydra.plugins.config import ConfigResult, ConfigSource, ObjectType

from .sources_registry import SourcesRegistry


class ConfigRepository:

    config_search_path: ConfigSearchPath
    sources: List[ConfigSource]

    def __init__(self, config_search_path: ConfigSearchPath) -> None:
        self.config_search_path = config_search_path
        self.sources = []
        for search_path in self.config_search_path.config_search_path:
            assert search_path.path is not None
            assert search_path.provider is not None
            scheme = self._get_scheme(search_path.path)
            source_type = SourcesRegistry.instance().resolve(scheme)
            self.sources.append(source_type(search_path.provider, search_path.path))

    def load_config(self, config_path: str) -> Optional[ConfigResult]:
        source = self._find_config(config_path=config_path)
        ret = None
        if source is not None:
            ret = source.load_config(config_path=config_path)
        return ret

    def exists(self, config_path: str) -> bool:
        return self._find_config(config_path) is not None

    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        options: List[str] = []
        for source in self.sources:
            object_type = source.get_type(config_path=group_name)
            if object_type == ObjectType.GROUP:
                options.extend(
                    source.list(config_path=group_name, results_filter=results_filter)
                )
        return sorted(list(set(options)))

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
