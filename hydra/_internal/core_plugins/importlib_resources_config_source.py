# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys
import zipfile
from typing import List, Optional

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource

if sys.version_info.major >= 4 or (
    sys.version_info.major >= 3 and sys.version_info.minor >= 9
):
    from importlib import resources
else:
    import importlib_resources as resources  # type:ignore

    # Relevant issue: https://github.com/python/mypy/issues/1153
    # Use importlib backport for Python older than 3.9


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
        res = resources.files(self.path).joinpath(normalized_config_path)  # type:ignore
        if not res.exists():
            raise ConfigLoadError(f"Config not found : {normalized_config_path}")

        try:
            if sys.version_info[0:2] >= (3, 8) and isinstance(res, zipfile.Path):
                f = res.open()
                header_text = f.read(512).decode("utf-8")
            else:
                f = res.open(encoding="utf-8")
                header_text = f.read(512)
            header = ConfigSource._get_header_dict(header_text)
            f.seek(0)
            cfg = OmegaConf.load(f)
        finally:
            f.close()

        self._update_package_in_header(
            header=header,
            normalized_config_path=normalized_config_path,
            is_primary_config=is_primary_config,
            package_override=package_override,
        )
        return ConfigResult(
            config=self._embed_config(cfg, header["package"]),
            path=f"{self.scheme()}://{self.path}",
            provider=self.provider,
            header=header,
        )

    def available(self) -> bool:
        try:
            ret = resources.is_resource(self.path, "__init__.py")  # type:ignore
            assert isinstance(ret, bool)
            return ret
        except ValueError:
            return False
        except ModuleNotFoundError:
            return False

    def is_group(self, config_path: str) -> bool:
        try:
            files = resources.files(self.path)  # type:ignore
        except Exception:
            return False

        res = files.joinpath(config_path)
        ret = res.exists() and res.is_dir()
        assert isinstance(ret, bool)
        return ret

    def is_config(self, config_path: str) -> bool:
        config_path = self._normalize_file_name(config_path)
        try:
            files = resources.files(self.path)  # type:ignore
        except Exception:
            return False
        res = files.joinpath(config_path)
        ret = res.exists() and res.is_file()
        assert isinstance(ret, bool)
        return ret

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        files: List[str] = []
        for file in (
            resources.files(self.path).joinpath(config_path).iterdir()  # type:ignore
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
