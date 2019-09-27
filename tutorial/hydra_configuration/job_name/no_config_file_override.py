# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra
from hydra import HydraConfig


@hydra.main()
def experiment(_cfg):
    print(HydraConfig().hydra.job.name)


if __name__ == "__main__":
    experiment()
