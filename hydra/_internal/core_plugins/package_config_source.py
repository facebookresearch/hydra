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
        full_path = f"{self.path}/{config_path}"
        module_name, resource_name = PackageConfigSource._split_module_and_resource(
            full_path
        )

        try:
            with resource_stream(module_name, resource_name) as stream:
                return ConfigResult(
                    config=OmegaConf.load(stream),
                    path=self.get_source_path(),
                    provider=self.provider,
                )
        except IOError:
            raise ConfigLoadError(f"PackageConfigSource: Config not found: {full_path}")

    def exists(self, config_path: str) -> bool:
        return self.get_type(config_path=config_path) != ObjectType.NOT_FOUND

    def get_type(self, config_path: str) -> ObjectType:
        full_path = self.concat(self.path, config_path)
        module_name, resource_name = PackageConfigSource._split_module_and_resource(
            full_path
        )

        try:
            if resource_exists(module_name, resource_name):
                if resource_isdir(module_name, resource_name):
                    return ObjectType.GROUP
                else:
                    return ObjectType.CONFIG
            else:
                return ObjectType.NOT_FOUND
        except NotImplementedError:
            raise NotImplementedError(
                "Unable to load {}/{}, are you missing an __init__.py?".format(
                    module_name, resource_name
                )
            )
        except ImportError:
            return ObjectType.NOT_FOUND

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

        return sorted(files)

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
