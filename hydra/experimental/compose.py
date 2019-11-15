# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra._internal.hydra import Hydra, GlobalHydra


def initialize_hydra(task_name, search_path_dir, strict):
    """
    Initializes the Hydra sub system

    :param task_name: The name of the task
    :param search_path_dir: entry point search path element (eg: /foo/bar or pkg://foo.bar)
    :param strict: Default value for strict mode
    """
    Hydra.create_main_hydra(
        task_name=task_name, strict=strict, search_path_dir=search_path_dir
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
    ), "GlobalHydra is not initialized, use @hydra.main() or call hydra.experimental.initialize_hydra() first"
    cfg = GlobalHydra().hydra.compose_config(
        config_file=config_file, overrides=overrides, strict=strict
    )
    del cfg["hydra"]
    return cfg
