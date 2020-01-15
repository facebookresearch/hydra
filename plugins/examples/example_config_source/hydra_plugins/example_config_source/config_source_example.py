# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Dict, List, Optional

from omegaconf import DictConfig

from hydra.core import Singleton
from hydra.core.object_type import ObjectType
from hydra.plugins.config.config_source import ConfigResult, ConfigSource
from hydra.plugins.config.errors import ConfigLoadError


class ConfigSourceExample(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        super().__init__(provider=provider, path=path)

    @staticmethod
    def scheme() -> str:
        return "example"

    def load_config(self, config_path: str) -> ConfigResult:
        return ConfigResult(
            config=ConfigStore.instance().load(config_path=config_path),
            path=f"{self.scheme()}://{self.path}",
            provider=self.provider,
        )

    def exists(self, config_path: str) -> bool:
        return self.get_type(config_path) is not ObjectType.NOT_FOUND

    def get_type(self, config_path: str) -> ObjectType:
        return ConfigStore.instance().get_type(config_path)

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        ret: List[str] = []
        files = ConfigStore.instance().list(config_path)

        for file in files:
            self._list_add_result(
                files=ret,
                file_path=f"{config_path}/{file}",
                file_name=file,
                results_filter=results_filter,
            )
        return ret


class ConfigStore(metaclass=Singleton):
    """
    Implements a simple in memory config store.
    """

    store: Dict[str, Any]

    def __init__(self) -> None:
        self.store = {}

    def mkdir(self, dir_path: str) -> None:
        assert dir_path.find("/") == -1
        if dir_path in self.store.keys():
            raise IOError(f"Already exists: {dir_path}")
        self.store[dir_path] = {}

    def add(self, path: str, name: str, node: DictConfig) -> None:
        d = self._open(path)
        if d is None or not isinstance(d, dict) or name in d:
            raise ConfigLoadError(f"Error adding {path}")

        d[name] = node

    def load(self, config_path: str) -> DictConfig:
        idx = config_path.rfind("/")
        if idx == -1:
            ret = self._open(config_path)
            assert isinstance(ret, DictConfig)
            return ret
        else:
            path = config_path[0:idx]
            name = config_path[idx + 1 :]
            d = self._open(path)
            if d is None or not isinstance(d, dict) or name not in d:
                raise ConfigLoadError(f"Error loading {config_path}")

            ret = d[name]
            assert isinstance(ret, DictConfig)
            return ret

    def get_type(self, path: str) -> ObjectType:
        d = self._open(path)
        if d is None:
            return ObjectType.NOT_FOUND
        if isinstance(d, dict):
            return ObjectType.GROUP
        else:
            return ObjectType.CONFIG

    def list(self, path: str) -> List[str]:
        d = self._open(path)
        if d is None:
            raise IOError(f"Path not found {path}")

        if not isinstance(d, dict):
            raise IOError(f"Path points to a file : {path}")

        return sorted(d.keys())

    def _open(self, path: str) -> Any:
        d: Any = self.store
        if path == "":
            return d

        for frag in path.split("/"):
            if frag == "":
                continue
            if frag not in d:
                return None
            d = d[frag]
        return d

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "ConfigStore":
        return Singleton.instance(ConfigStore, *args, **kwargs)  # type: ignore
