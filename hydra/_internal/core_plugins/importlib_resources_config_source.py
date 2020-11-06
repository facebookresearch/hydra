# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from typing import List, Optional

import importlib_resources
from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource


class ImportlibResourcesConfigSource(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        super().__init__(provider=provider, path=path)
        # normalize to pkg format
        self.path = self.path.replace("/", ".").rstrip(".")

    @staticmethod
    def scheme() -> str:
        return "pkg"

    def load_config(
        self,
        config_path: str,
        is_primary_config: bool,
        package_override: Optional[str] = None,
    ) -> ConfigResult:
        normalized_config_path = self._normalize_file_name(config_path)
        res = importlib_resources.files(self.path).joinpath(normalized_config_path)
        if not res.exists():
            raise ConfigLoadError(f"Config not found : {normalized_config_path}")

        with open(res, encoding="utf-8") as f:
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
        try:
            ret = importlib_resources.is_resource(self.path, "__init__.py")
            assert isinstance(ret, bool)
            return ret
        except ValueError:
            return False
        except ModuleNotFoundError:
            return False

    def is_group(self, config_path: str) -> bool:
        try:
            files = importlib_resources.files(self.path)
        except Exception:
            return False

        res = files.joinpath(config_path)
        ret = res.exists() and res.is_dir()
        assert isinstance(ret, bool)
        return ret

    def is_config(self, config_path: str) -> bool:
        config_path = self._normalize_file_name(config_path)
        try:
            files = importlib_resources.files(self.path)
        except Exception:
            return False
        res = files.joinpath(config_path)
        ret = res.exists() and res.is_file()
        assert isinstance(ret, bool)
        return ret

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        files: List[str] = []
        for file in (
            importlib_resources.files(self.path).joinpath(config_path).iterdir()
        ):
            fname = file.name
            fpath = os.path.join(config_path, fname)
            self._list_add_result(
                files=files,
                file_path=fpath,
                file_name=fname,
                results_filter=results_filter,
            )

        return sorted(list(set(files)))
