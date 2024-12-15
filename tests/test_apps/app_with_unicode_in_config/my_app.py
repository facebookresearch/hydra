# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys

from omegaconf import DictConfig, OmegaConf

import hydra


@hydra.main(version_base=None, config_path=".", config_name="config")
def my_app(cfg: DictConfig) -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
