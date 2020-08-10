# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import time
from pathlib import Path
from typing import Tuple

from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig
from hydra.utils import get_original_cwd


@hydra.main(config_name="config")
def my_app(_: DictConfig) -> None:
    run_dir = Path.cwd().relative_to(get_original_cwd())
    time.sleep(5)
    run_dir_after_sleep = HydraConfig.get().run.dir
    print(run_dir)
    print(run_dir_after_sleep)


if __name__ == "__main__":
    my_app()
