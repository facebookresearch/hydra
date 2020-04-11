# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig


@hydra.main()
def experiment(_cfg: DictConfig) -> None:
    hc = HydraConfig.instance()
    assert hc.hydra is not None
    print(hc.hydra.job.name)


if __name__ == "__main__":
    experiment()
