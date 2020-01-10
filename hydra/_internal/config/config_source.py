# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from omegaconf import Container


@dataclass
class ConfigResult:
    provider: str
    path: str
    config: Container


class ObjectType(Enum):
    NOT_FOUND = 0
    CONFIG = 1
    GROUP = 2


class ConfigSource(ABC):
    provider: str
    path: str

    @abstractmethod
    def __init__(self, provider: str, path: str) -> None:
        ...

    @abstractmethod
    def load_config(self, config_path: str) -> ConfigResult:
        ...

    @abstractmethod
    def exists(self, config_path: str) -> bool:
        ...

    def get_type(self, config_path: str) -> ObjectType:
        ...

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        ...

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"provider={self.provider}, path={self.path}"

    def _list_add_result(
        self,
        files: List[str],
        file_path: str,
        file_name: str,
        results_filter: Optional[ObjectType],
    ) -> None:
        file_type = self.get_type(file_path)
        assert file_type is not ObjectType.NOT_FOUND
        if (
            file_type == ObjectType.GROUP
            and (results_filter is None or results_filter == ObjectType.GROUP)
            and file_name != "__pycache__"
        ):
            files.append(file_name)
        if (
            file_type == ObjectType.CONFIG
            and file_name.endswith(".yaml")
            and (results_filter is None or results_filter == ObjectType.CONFIG)
        ):
            files.append(file_name[0 : -len(".yaml")])
