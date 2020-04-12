# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig


@hydra.main(config_path="config.yaml")
def experiment(_cfg: DictConfig) -> None:
    print(HydraConfig.get().job.name)


if __name__ == "__main__":
    experiment()
