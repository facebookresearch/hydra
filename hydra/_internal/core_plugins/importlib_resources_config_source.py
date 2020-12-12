# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys
from typing import List, Optional

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource

if sys.version_info[0] == 3 and sys.version_info[1] < 9:
    import importlib_resources

    # `importlib_resources` is avilable only till Python 3.8. Beyond this,
    # one should use `importlib.resources`.
    # Note that `importlib.resources` is available on Python 3.8 but its
    # API does not match the API of `importlib_resources`. However, in
    # Python 3.9, the API of `importlib.resources` matches the API of
    # `importlib_resources`.
    # So, by default, we try to use `importlib_resources` (supported till 3.8)
    # and if that is not found, we use `importlib.resources`.
    # Switching the order of import statements breaks the code for Python 3.8.
else:
    from importlib import resources as importlib_resources


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

        with res.open(encoding="utf-8") as f:
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
            defaults_list = self._extract_defaults_list(
                config_path=config_path, cfg=cfg
            )
            return ConfigResult(
                config=self._embed_config(cfg, header["package"]),
                path=f"{self.scheme()}://{self.path}",
                provider=self.provider,
                header=header,
                defaults_list=defaults_list,
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
