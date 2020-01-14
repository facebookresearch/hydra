# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra
from hydra.plugins.common.utils import HydraConfig


@hydra.main(config_path="config.yaml")
def experiment(_cfg):
    print(HydraConfig.instance().hydra.job.name)


if __name__ == "__main__":
    experiment()
