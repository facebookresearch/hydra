# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path

from hydra.experimental import (
    initialize,
    initialize_config_dir,
    initialize_config_module,
)


def hydra_initialize() -> None:
    initialize(config_path="../../hydra/test_utils/configs")


def hydra_initialize_config_dir() -> None:
    abs_conf_dir = Path.cwd() / "../../hydra/test_utils/configs"
    initialize_config_dir(config_dir=str(abs_conf_dir))


def hydra_initialize_config_module() -> None:
    initialize_config_module(config_module="hydra.test_utils.configs")
