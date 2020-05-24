# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(config_path="configs/completion_test", config_name="config")
def run_cli(cfg: DictConfig) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    run_cli()
