# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra._internal.core_plugins.importlib_resources_config_source import (
    ImportlibResourcesConfigSource,
)
from hydra.core.global_hydra import GlobalHydra
from hydra.experimental import initialize
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra.test_utils.test_utils import chdir_plugin_root

chdir_plugin_root()


@pytest.mark.parametrize(
    "type_, path",
    [
        pytest.param(
            ImportlibResourcesConfigSource,
            "pkg://some_namespace.namespace_test.dir",
            id="pkg_in_namespace",
        ),
    ],
)
class TestCoreConfigSources(ConfigSourceTestSuite):
    pass


def test_config_in_dir() -> None:
    with initialize(config_path="../some_namespace/namespace_test/dir"):
        config_loader = GlobalHydra.instance().config_loader()
        assert "cifar10" in config_loader.get_group_options("dataset")
        assert "imagenet" in config_loader.get_group_options("dataset")
        assert "level1" in config_loader.list_groups("")
        assert "level2" in config_loader.list_groups("level1")
        assert "nested1" in config_loader.get_group_options("level1/level2")
        assert "nested2" in config_loader.get_group_options("level1/level2")
