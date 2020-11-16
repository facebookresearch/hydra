# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Optional

from omegaconf import DictConfig


class Callback:
    """
    Provides callbacks through different life cycle events of an Hydra application.
    """

    config: Optional[DictConfig]

    def pre_run(self, cfg: DictConfig) -> None:
        ...

    def post_run(self, cfg: DictConfig) -> None:
        ...

    def pre_sweep(self, sweep_cfg: DictConfig) -> None:
        ...

    def post_sweep(self, sweep_cfg: DictConfig) -> None:
        ...

    def pre_job(self, job_cfg: DictConfig) -> None:
        ...

    def post_job(self, job_cfg: DictConfig) -> None:
        ...
