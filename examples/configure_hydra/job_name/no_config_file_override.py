# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main()
def experiment(_cfg: DictConfig) -> None:
    print(hydra.core.hydra_config.HydraConfig.instance().hydra.job.name)


if __name__ == "__main__":
    experiment()
