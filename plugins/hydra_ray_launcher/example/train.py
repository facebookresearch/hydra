# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
from pathlib import Path

import hydra
from omegaconf import DictConfig

from model.my_model import MyModel

log = logging.getLogger(__name__)


@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    log.info("Start training...")
    model = MyModel(cfg.random_seed)
    # save checkpoint to current working dir.
    model.save(Path(os.getcwd()) / cfg.get("checkpoint_path"))


if __name__ == "__main__":
    main()
