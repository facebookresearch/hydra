# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main()  # NOTE: version_base parameter intentionally omitted
def my_app(_: DictConfig) -> None:
    pass


if __name__ == "__main__":
    my_app()
