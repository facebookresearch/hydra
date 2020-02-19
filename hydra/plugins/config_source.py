# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from omegaconf import Container

from hydra.core.object_type import ObjectType
from hydra.plugins.plugin import Plugin


@dataclass
class ConfigResult:
    provider: str
    path: str
    config: Container
    is_schema_source: bool = False


class ConfigLoadError(IOError):
    pass


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

    # subclasses may override to improve performance
    def exists(self, config_path: str) -> bool:
        return self.is_group(config_path) or self.is_config(config_path)

    @abstractmethod
    def is_group(self, config_path: str) -> bool:
        ...

    @abstractmethod
    def is_config(self, config_path: str) -> bool:
        ...

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        """
        List items under the specified config path
        :param config_path: config path to list items in, examples: "", "foo", "foo/bar"
        :param results_filter: None for all, GROUP for groups only and CONFIG for configs only
        :return: a list of config or group identifiers (sorted and unique)
        """
        ...

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"provider={self.provider}, path={self.scheme()}://{self.path}"

    def _list_add_result(
        self,
        files: List[str],
        file_path: str,
        file_name: str,
        results_filter: Optional[ObjectType],
    ) -> None:
        filtered = ["__pycache__", "__init__.py"]
        is_group = self.is_group(file_path)
        is_config = self.is_config(file_path)
        if (
            is_group
            and (results_filter is None or results_filter == ObjectType.GROUP)
            and file_name not in filtered
        ):
            files.append(file_name)
        if (
            is_config
            and file_name not in filtered
            and (results_filter is None or results_filter == ObjectType.CONFIG)
        ):
            # strip extension
            last_dot = file_name.rfind(".")
            if last_dot != -1:
                file_name = file_name[0:last_dot]

            files.append(file_name)

    def full_path(self) -> str:
        return f"{self.scheme()}://{self.path}"

    @staticmethod
    def _normalize_file_name(filename: str) -> str:
        if not any(filename.endswith(ext) for ext in [".yaml", ".yml"]):
            filename += ".yaml"
        return filename
