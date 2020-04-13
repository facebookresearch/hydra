#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(config_path="config.yaml")
def main(cfg: DictConfig) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    main()
