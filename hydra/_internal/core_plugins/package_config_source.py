# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional, Tuple

from omegaconf import OmegaConf
from pkg_resources import (
    resource_exists,
    resource_isdir,
    resource_listdir,
    resource_stream,
)

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource


class PackageConfigSource(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        super().__init__(provider=provider, path=path)

    @staticmethod
    def scheme() -> str:
        return "pkg"

    def load_config(self, config_path: str) -> ConfigResult:
        config_path = self._normalize_file_name(filename=config_path)
        module_name, resource_name = PackageConfigSource._split_module_and_resource(
            self.concat(self.path, config_path)
        )

        try:
            with resource_stream(module_name, resource_name) as stream:
                return ConfigResult(
                    config=OmegaConf.load(stream),
                    path=f"{self.scheme()}://{self.path}",
                    provider=self.provider,
                )
        except FileNotFoundError:
            raise ConfigLoadError(
                f"PackageConfigSource: Config not found: module={module_name}, resource_name={resource_name}"
            )

    @staticmethod
    def _exists(module_name: str, resource_name: str) -> bool:
        try:
            if resource_exists(module_name, resource_name):
                return True
        except NotImplementedError:
            return False
        except ImportError:
            return False
        return False

    def is_group(self, config_path: str) -> bool:
        module_name, resource_name = PackageConfigSource._split_module_and_resource(
            self.concat(self.path, config_path)
        )
        return self._exists(module_name, resource_name) and resource_isdir(
            module_name, resource_name
        )

    def is_config(self, config_path: str) -> bool:
        config_path = self._normalize_file_name(filename=config_path)
        fname = self.concat(self.path, config_path)
        module_name, resource_name = PackageConfigSource._split_module_and_resource(
            fname
        )
        return self._exists(module_name, resource_name) and not resource_isdir(
            module_name, resource_name
        )

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        files: List[str] = []
        full_path = self.concat(self.path, config_path)
        module_name, resource_name = PackageConfigSource._split_module_and_resource(
            full_path
        )
        for file in resource_listdir(module_name, resource_name):
            file_path = self.concat(config_path, file)
            self._list_add_result(
                files=files,
                file_path=file_path,
                file_name=file,
                results_filter=results_filter,
            )

        return sorted(list(set(files)))

    @staticmethod
    def _split_module_and_resource(filename: str) -> Tuple[str, str]:
        sep = filename.find("/")
        if sep == -1:
            module_name = filename
            resource_name = ""
        else:
            module_name = filename[0:sep]
            resource_name = filename[sep + 1 :]
        if module_name == "":
            # if we have a module a module only, dirname would return nothing and basename would return the module.
            module_name = resource_name
            resource_name = ""

        return module_name, resource_name

    @staticmethod
    def concat(path1: str, path2: str) -> str:
        if path1 != "":
            return f"{path1}/{path2}"
        else:
            return path2
