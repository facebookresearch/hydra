# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# DEPRECATED: remove in 1.2
from typing import List, Optional

from omegaconf import DictConfig

from hydra._internal.deprecation_warning import deprecation_warning


def compose(
    config_name: Optional[str] = None,
    overrides: List[str] = [],
    return_hydra_config: bool = False,
    strict: Optional[bool] = None,
) -> DictConfig:
    from hydra import compose as real_compose

    deprecation_warning(
        message="hydra.experimental.compose() is no longer experimental."
        " Use hydra.compose()",
    )
    return real_compose(
        config_name=config_name,
        overrides=overrides,
        return_hydra_config=return_hydra_config,
        strict=strict,
    )
