# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import List, Optional

from omegaconf import DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class Config:
    list: Optional[List[int]] = None


cs = ConfigStore.instance()
cs.store(name="config", node=Config)


@hydra.main(version_base=None, config_name="config")
def main(cfg: DictConfig) -> None:
    print(cfg)


if __name__ == "__main__":
    main()
