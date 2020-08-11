# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import time
from pathlib import Path

from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig
from hydra.utils import get_original_cwd


@hydra.main()
def my_app(_: DictConfig) -> None:
    run_dir = str(Path.cwd().relative_to(get_original_cwd()))
    time.sleep(2)
    run_dir_after_sleep = HydraConfig.get().run.dir
    print(run_dir)
    print(type(run_dir))
    print(run_dir_after_sleep)
    print(type(run_dir_after_sleep))
    assert run_dir == run_dir_after_sleep


if __name__ == "__main__":
    my_app()
