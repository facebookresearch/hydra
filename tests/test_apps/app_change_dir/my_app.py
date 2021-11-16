# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from pathlib import Path

from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig


@hydra.main(config_path=None)
def main(_: DictConfig):
    subdir = Path(HydraConfig.get().run.dir) / Path("subdir")
    subdir.mkdir(exist_ok=True, parents=True)
    os.chdir(subdir)


if __name__ == "__main__":
    main()

print(f"current dir: {os.getcwd()}")
