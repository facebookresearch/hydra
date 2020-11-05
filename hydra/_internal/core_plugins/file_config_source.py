# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from typing import List, Optional

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource


class FileConfigSource(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        if path.find("://") == -1:
            path = f"{self.scheme()}://{path}"
        super().__init__(provider=provider, path=path)

    @staticmethod
    def scheme() -> str:
        return "file"

    def load_config(
        self,
        config_path: str,
        is_primary_config: bool,
        package_override: Optional[str] = None,
    ) -> ConfigResult:
        normalized_config_path = self._normalize_file_name(config_path)
        full_path = os.path.realpath(os.path.join(self.path, normalized_config_path))
        if not os.path.exists(full_path):
            raise ConfigLoadError(f"Config not found : {full_path}")

        with open(full_path, encoding="utf-8") as f:
            header_text = f.read(512)
            header = ConfigSource._get_header_dict(header_text)
            self._update_package_in_header(
                header=header,
                normalized_config_path=normalized_config_path,
                is_primary_config=is_primary_config,
                package_override=package_override,
            )
            f.seek(0)
            cfg = OmegaConf.load(f)
            return ConfigResult(
                config=self._embed_config(cfg, header["package"]),
                path=f"{self.scheme()}://{self.path}",
                provider=self.provider,
                header=header,
            )

    def available(self) -> bool:
        return self.is_group("")

    def is_group(self, config_path: str) -> bool:
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        return os.path.isdir(full_path)

    def is_config(self, config_path: str) -> bool:
        config_path = self._normalize_file_name(config_path)
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        return os.path.isfile(full_path)

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

        return sorted(list(set(files)))
