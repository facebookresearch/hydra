# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from typing import Any

from omegaconf import DictConfig, OmegaConf

from hydra.core.singleton import Singleton


class HydraConfig(metaclass=Singleton):
    hydra: DictConfig

    def __init__(self) -> None:
        ret = OmegaConf.create()
        assert isinstance(ret, DictConfig)
        self.hydra = ret

    def set_config(self, cfg: DictConfig) -> None:
        try:
            OmegaConf.set_readonly(self.hydra, False)
            self.hydra = copy.deepcopy(cfg.hydra)
        finally:
            OmegaConf.set_readonly(self.hydra, True)

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "HydraConfig":
        return Singleton.instance(HydraConfig, *args, **kwargs)  # type: ignore
