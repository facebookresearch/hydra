# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from omegaconf import DictConfig, open_dict

from hydra.core.global_hydra import GlobalHydra
from hydra.types import RunMode


def compose(
    config_name: Optional[str] = None,
    overrides: List[str] = [],
    strict: Optional[bool] = None,
    return_hydra_config: bool = False,
) -> DictConfig:
    """
    :param config_name: the name of the config
           (usually the file name without the .yaml extension)
    :param overrides: list of overrides for config file
    :param strict: optionally override the default strict mode
    :param return_hydra_config: True to return the hydra config node in the result
    :return: the composed config
    """
    assert GlobalHydra().is_initialized(), (
        "GlobalHydra is not initialized, use @hydra.main()"
        " or call one of the hydra.experimental initialize methods first"
    )

    gh = GlobalHydra.instance()
    assert gh.hydra is not None
    cfg = gh.hydra.compose_config(
        config_name=config_name,
        overrides=overrides,
        run_mode=RunMode.RUN,
        strict=strict,
        from_shell=False,
        with_log_configuration=False,
    )
    assert isinstance(cfg, DictConfig)

    if not return_hydra_config:
        if "hydra" in cfg:
            with open_dict(cfg):
                del cfg["hydra"]
    return cfg
