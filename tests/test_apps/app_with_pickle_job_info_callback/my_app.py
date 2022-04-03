# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging
import pickle
from pathlib import Path
from typing import Any

from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path=".", config_name="config")
def my_app(cfg: DictConfig) -> str:
    def pickle_cfg(path: Path, obj: Any) -> Any:
        with open(str(path), "wb") as file:
            pickle.dump(obj, file)

    hydra_cfg = HydraConfig.get()
    output_dir = Path(hydra_cfg.runtime.output_dir)
    pickle_cfg(Path(output_dir) / "task_cfg.pickle", cfg)
    pickle_cfg(Path(output_dir) / "hydra_cfg.pickle", hydra_cfg)
    log.info("Running my_app")

    return "hello world"


if __name__ == "__main__":
    my_app()
