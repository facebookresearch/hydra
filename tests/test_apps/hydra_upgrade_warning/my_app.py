# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings

from omegaconf import DictConfig

import hydra
from hydra.errors import HydraUpgradeWarning


@hydra.main(config_path=None)
def my_app(cfg: DictConfig) -> None:
    warnings.warn("Feature FooBarBaz is deprecated", category=HydraUpgradeWarning)


if __name__ == "__main__":
    my_app()
