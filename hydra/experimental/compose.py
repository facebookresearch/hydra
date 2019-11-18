# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra._internal.hydra import Hydra, GlobalHydra
from hydra._internal.utils import detect_calling_file_or_module


def initialize(config_dir=None, strict=None, caller_stack_depth=1):
    """
    :param config_dir: config directory relative to the calling script
    :param strict:
    :param caller_stack_depth:
    :return:
    """
    calling_file, calling_module = detect_calling_file_or_module(caller_stack_depth + 1)
    Hydra.create_main_hydra_file_or_module(
        calling_file, calling_module, config_dir, strict
    )


def compose(config_file=None, overrides=[], strict=None):
    """
    :param config_file: optional config file to load
    :param overrides: list of overrides for config file
    :param strict: optionally override the default strict mode
    :return: the composed config
    """
    assert (
        GlobalHydra().is_initialized()
    ), "GlobalHydra is not initialized, use @hydra.main() or call hydra.experimental.initialize() first"

    cfg = GlobalHydra().hydra.compose_config(
        config_file=config_file, overrides=overrides, strict=strict
    )
    if "hydra" in cfg:
        del cfg["hydra"]
    return cfg
