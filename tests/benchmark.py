# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from typing import Any

from pytest import fixture

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.utils import create_config_search_path
from hydra.types import RunMode


@fixture(scope="module")
def config_loader() -> Any:
    return ConfigLoaderImpl(
        config_search_path=create_config_search_path("pkg://hydra.test_utils.configs")
    )


def test_config_loading(config_loader: ConfigLoaderImpl, benchmark: Any) -> None:
    benchmark(
        config_loader.load_configuration,
        "config",
        overrides=[],
        run_mode=RunMode.RUN,
    )
