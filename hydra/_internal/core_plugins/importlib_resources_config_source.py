# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys
import zipfile
from typing import TYPE_CHECKING, Any, List, Optional

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource

if TYPE_CHECKING or (sys.version_info < (3, 9)):
    import importlib_resources as resources
else:
    from importlib import resources

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

    def _read_config(self, res: Any) -> ConfigResult:
        try:
            if sys.version_info[0:2] >= (3, 8) and isinstance(res, zipfile.Path):
                # zipfile does not support encoding, read() calls returns bytes.
                f = res.open()
            else:
                f = res.open(encoding="utf-8")
            header_text = f.read(512)
            if isinstance(header_text, bytes):
                # if header is bytes, utf-8 decode (zipfile path)
                header_text = header_text.decode("utf-8")
            header = ConfigSource._get_header_dict(header_text)
            f.seek(0)
            cfg = OmegaConf.load(f)
            return ConfigResult(
                config=cfg,
                path=f"{self.scheme()}://{self.path}",
                provider=self.provider,
                header=header,
            )
        finally:
            f.close()

    def load_config(self, config_path: str) -> ConfigResult:
        normalized_config_path = self._normalize_file_name(config_path)
        res = resources.files(self.path).joinpath(normalized_config_path)
        if not res.exists():
            raise ConfigLoadError(f"Config not found : {normalized_config_path}")

        return self._read_config(res)

    def available(self) -> bool:
        try:
            files = resources.files(self.path)
        except (ValueError, ModuleNotFoundError, TypeError):
            return False
        return any(f.name == "__init__.py" and f.is_file() for f in files.iterdir())

    def is_group(self, config_path: str) -> bool:
        try:
            files = resources.files(self.path)
        except (ValueError, ModuleNotFoundError, TypeError):
            return False

        res = files.joinpath(config_path)
        ret = res.exists() and res.is_dir()
        assert isinstance(ret, bool)
        return ret

    def is_config(self, config_path: str) -> bool:
        config_path = self._normalize_file_name(config_path)
        try:
            files = resources.files(self.path)
        except (ValueError, ModuleNotFoundError, TypeError):
            return False
        res = files.joinpath(config_path)
        ret = res.exists() and res.is_file()
        assert isinstance(ret, bool)
        return ret

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        files: List[str] = []
        for file in resources.files(self.path).joinpath(config_path).iterdir():
            fname = file.name
            fpath = os.path.join(config_path, fname)
            self._list_add_result(
                files=files,
                file_path=fpath,
                file_name=fname,
                results_filter=results_filter,
            )

        return sorted(list(set(files)))
