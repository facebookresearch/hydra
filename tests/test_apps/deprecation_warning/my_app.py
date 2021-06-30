# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(config_path=None)
def my_app(cfg: DictConfig) -> None:
    hydra._internal.utils2.deprecation_warning("Feature FooBar is deprecated")


if __name__ == "__main__":
    my_app()
