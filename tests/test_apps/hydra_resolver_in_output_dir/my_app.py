# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig


@hydra.main(config_path=None)
def my_app(_: DictConfig) -> None:
    print(HydraConfig.instance().get().runtime.output_dir)


if __name__ == "__main__":
    my_app()
