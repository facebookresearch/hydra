# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from omegaconf import DictConfig


def compose(
    config_name: Optional[str] = None,
    overrides: List[str] = [],
    return_hydra_config: bool = False,
    strict: Optional[bool] = None,
) -> DictConfig:
    message = (
        "hydra.experimental.compose() is no longer experimental. Use hydra.compose()"
    )
    raise ImportError(message)
