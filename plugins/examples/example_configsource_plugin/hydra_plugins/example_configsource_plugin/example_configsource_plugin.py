# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Dict, List, Optional

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource
from omegaconf import OmegaConf


class ConfigSourceExample(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        super().__init__(provider=provider, path=path)
        self.configs: Dict[str, Dict[str, Any]] = {
            "config_without_group": {"group": False},
            "dataset/imagenet": {
                "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
            },
            "dataset/cifar10": {
                "dataset": {"name": "cifar10", "path": "/datasets/cifar10"}
            },
            "level1/level2/nested1": {},
            "level1/level2/nested2": {},
        }

    @staticmethod
    def scheme() -> str:
        return "example"

    def load_config(self, config_path: str) -> ConfigResult:
        if config_path not in self.configs:
            raise ConfigLoadError("Config not found : " + config_path)
        return ConfigResult(
            config=OmegaConf.create(self.configs[config_path]),
            path=f"{self.scheme()}://{self.path}",
            provider=self.provider,
        )

    def is_group(self, config_path: str) -> bool:
        groups = {"", "dataset", "optimizer", "level1", "level1/level2"}
        return config_path in groups

    def is_config(self, config_path: str) -> bool:
        base = {
            "dataset",
            "dataset/imagenet",
            "level1/level2/nested1",
            "level1/level2/nested2",
        }
        configs = set([x for x in base] + [f"{x}.yaml" for x in base])
        return config_path in configs

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:

        groups: Dict[str, List[str]] = {
            "": ["dataset", "level1", "optimizer"],
            "dataset": [],
            "optimizer": [],
            "level1": ["level2"],
            "level1/level2": [],
        }
        configs: Dict[str, List[str]] = {
            "": ["config_without_group", "dataset"],
            "dataset": ["cifar10", "imagenet"],
            "optimizer": ["adam", "nesterov"],
            "level1": [],
            "level1/level2": ["nested1", "nested2"],
        }
        if results_filter is None:
            return sorted(set(groups[config_path] + configs[config_path]))
        elif results_filter == ObjectType.GROUP:
            return groups[config_path]
        elif results_filter == ObjectType.CONFIG:
            return configs[config_path]
        else:
            raise ValueError()
