# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from omegaconf import DictConfig

from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigSource


@dataclass
class LoadTrace:
    filename: str
    path: Optional[str]
    provider: Optional[str]
    schema_provider: Optional[str] = None


class ConfigLoader(ABC):
    """
    Config loader interface
    """

    @abstractmethod
    def load_configuration(
        self,
        config_name: Optional[str],
        overrides: List[str],
        strict: Optional[bool] = None,
    ) -> DictConfig:
        ...

    @abstractmethod
    def load_sweep_config(
        self, master_config: DictConfig, sweep_overrides: List[str]
    ) -> DictConfig:
        ...

    @abstractmethod
    def get_search_path(self) -> ConfigSearchPath:
        ...

    @abstractmethod
    def get_load_history(self) -> List[LoadTrace]:
        ...

    @abstractmethod
    def get_sources(self) -> List[ConfigSource]:
        ...

    @abstractmethod
    def list_groups(self, parent_name: str) -> List[str]:
        ...

    @abstractmethod
    def get_group_options(
        self, group_name: str, results_filter: Optional[ObjectType] = ObjectType.CONFIG
    ) -> List[str]:
        ...
