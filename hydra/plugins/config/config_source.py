# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import abstractmethod
from typing import List, Optional

from hydra.plugins.plugin import Plugin

from .config_resullt import ConfigResult
from .object_type import ObjectType


class ConfigSource(Plugin):
    provider: str
    path: str

    def __init__(self, provider: str, path: str) -> None:
        if not path.startswith(self.scheme()):
            raise ValueError("Invalid path")
        self.provider = provider
        self.path = path[len(self.scheme() + "://") :]

    @staticmethod
    @abstractmethod
    def scheme() -> str:
        """
        :return: the scheme for this config source, for example file:// or pkg://
        """
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
        filtered = ["__pycache__", "__init__.py"]
        file_type = self.get_type(file_path)
        assert file_type is not ObjectType.NOT_FOUND
        if (
            file_type == ObjectType.GROUP
            and (results_filter is None or results_filter == ObjectType.GROUP)
            and file_name not in filtered
        ):
            files.append(file_name)
        if (
            file_type == ObjectType.CONFIG
            and file_name not in filtered
            and (results_filter is None or results_filter == ObjectType.CONFIG)
        ):
            last_dot = file_name.rfind(".")
            if last_dot != -1:
                file_name = file_name[0:last_dot]
            files.append(file_name)
