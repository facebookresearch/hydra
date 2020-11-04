from dataclasses import dataclass

from typing import Optional, List

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class Config:
    list: Optional[List[int]] = None


cs = ConfigStore.instance()
cs.store(name="config", node=Config)


@hydra.main(config_name="config")
def main(cfg):
    print(cfg)


if __name__ == "__main__":
    main()
