# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Dict, List, Optional

from omegaconf import DictConfig, OmegaConf

from hydra.core.object_type import ObjectType
from hydra.core.singleton import Singleton
from hydra.plugins.config_source import ConfigLoadError


class StructuredConfigStore(metaclass=Singleton):
    repo: Dict[str, Any]

    def __init__(self) -> None:
        self.repo = {}

    def store(
        self, group: Optional[str], name: str, path: Optional[str], node: Any
    ) -> None:
        """
        Stores a config node into the repository
        :rtype: object
        :param group:
        :param name:
        :param path:
        :param node:
        :return:
        """
        cur = self.repo
        if group is not None:
            for d in group.split("/"):
                if d not in cur:
                    cur[d] = {}
                cur = cur[d]

        if path is not None and path != "":
            cfg = OmegaConf.create()
            cfg.update_node(path, OmegaConf.structured(node))
        else:
            cfg = OmegaConf.structured(node)

        cur[f"{name}.yaml"] = cfg

    def load(self, config_path: str) -> DictConfig:
        idx = config_path.rfind("/")
        if idx == -1:
            ret = self._open(config_path)
            if ret is None:
                raise ConfigLoadError(f"Structured config not found {config_path}")

            assert isinstance(ret, DictConfig)
            return ret
        else:
            path = config_path[0:idx]
            name = config_path[idx + 1 :]
            d = self._open(path)
            if d is None or not isinstance(d, dict):
                raise ConfigLoadError(f"Structured config not found {config_path}")

            if name not in d:
                raise ConfigLoadError(
                    f"Structured config {name} not found in {config_path}"
                )

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
        d: Any = self.repo
        for frag in path.split("/"):
            if frag == "":
                continue
            if frag in d:
                d = d[frag]
            else:
                return None
        return d

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "StructuredConfigStore":
        return Singleton.instance(StructuredConfigStore, *args, **kwargs)  # type: ignore
