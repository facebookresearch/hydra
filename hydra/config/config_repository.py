# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import ABC, abstractmethod
from typing import List, Optional

from hydra.plugins.config import ConfigResult, ConfigSource, ObjectType


class ConfigRepository(ABC):
    @abstractmethod
    def load_config(self, config_path: str) -> Optional[ConfigResult]:
        ...

    @abstractmethod
    def exists(self, config_path: str) -> bool:
        ...

    @abstractmethod
    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        ...

    @abstractmethod
    def get_sources(self) -> List[ConfigSource]:
        ...
