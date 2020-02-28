# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from typing import Any

from omegaconf import DictConfig, OmegaConf

from hydra.conf import HydraConf
from hydra.core.singleton import Singleton


class HydraConfig(metaclass=Singleton):
    hydra: HydraConf

    def __init__(self) -> None:
        ret = OmegaConf.structured(HydraConf)
        self.hydra = ret

    def set_config(self, cfg: DictConfig) -> None:
        self.hydra = copy.deepcopy(cfg.hydra)
        OmegaConf.set_readonly(self.hydra, True)  # type: ignore

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "HydraConfig":
        return Singleton.instance(HydraConfig, *args, **kwargs)  # type: ignore
