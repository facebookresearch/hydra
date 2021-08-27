# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(config_path=".", config_name="config")
def my_app(config: DictConfig) -> None:
    print(f"letter={config.letter} number={config.number}")


if __name__ == "__main__":
    my_app()
