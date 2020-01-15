# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra
from hydra.core import HydraConfig


@hydra.main()
def experiment(_cfg: DictConfig) -> None:
    print(HydraConfig.instance().hydra.job.name)


if __name__ == "__main__":
    experiment()
