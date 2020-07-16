# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


def foo(cfg: DictConfig) -> None:
    cfg.foo = "bar"  # does not exist in the config


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    foo(cfg)


if __name__ == "__main__":
    my_app()
