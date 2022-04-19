# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra
from hydra._internal.deprecation_warning import deprecation_warning


@hydra.main(version_base=None)
def my_app(cfg: DictConfig) -> None:
    deprecation_warning("Feature FooBar is deprecated")


if __name__ == "__main__":
    my_app()
