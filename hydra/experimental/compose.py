# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# DEPRECATED: remove in 1.2
import warnings
from typing import List, Optional

from omegaconf import DictConfig


def compose(
    config_name: Optional[str] = None,
    overrides: List[str] = [],
    return_hydra_config: bool = False,
) -> DictConfig:
    from hydra import compose as real_compose

    warnings.warn(
        category=UserWarning,
        message="hydra.experimental.compose() is no longer experimental."
        " Use hydra.compose()",
    )
    return real_compose(
        config_name=config_name,
        overrides=overrides,
        return_hydra_config=return_hydra_config,
    )
