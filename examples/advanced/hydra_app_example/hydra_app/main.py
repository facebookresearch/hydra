#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(config_path="config.yaml")
def main(cfg: DictConfig) -> None:
    print(cfg.pretty())


# this function is required to allow automatic detection of the module name when running
# from a binary script.
# it should be called from the executable script and not the hydra.main() function directly.
def entry() -> None:
    main()


if __name__ == "__main__":
    main()
