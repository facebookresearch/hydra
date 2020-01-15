# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from typing import List, Optional

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config.config_source import ConfigResult, ConfigSource
from hydra.plugins.config.errors import ConfigLoadError


class FileConfigSource(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        if path.find("://") == -1:
            path = f"{self.scheme()}://{path}"
        super().__init__(provider=provider, path=path)

    @staticmethod
    def scheme() -> str:
        return "file"

    def load_config(self, config_path: str) -> ConfigResult:
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        if not os.path.exists(full_path):
            raise ConfigLoadError(f"FileConfigSource: Config not found : {full_path}")
        return ConfigResult(
            config=OmegaConf.load(full_path),
            path=f"{self.scheme()}://{self.path}",
            provider=self.provider,
        )

    def exists(self, config_path: str) -> bool:
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        return os.path.exists(full_path)

    def get_type(self, config_path: str) -> ObjectType:
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                return ObjectType.GROUP
            else:
                return ObjectType.CONFIG
        else:
            return ObjectType.NOT_FOUND

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        files: List[str] = []
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        for file in os.listdir(full_path):
            file_path = os.path.join(config_path, file)
            self._list_add_result(
                files=files,
                file_path=file_path,
                file_name=file,
                results_filter=results_filter,
            )

        return sorted(files)
