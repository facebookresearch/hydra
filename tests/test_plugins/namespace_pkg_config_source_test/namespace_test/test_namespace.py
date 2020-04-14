# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

import pytest

from hydra._internal.core_plugins.package_config_source import PackageConfigSource
from hydra.core.global_hydra import GlobalHydra
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra.test_utils.test_utils import chdir_plugin_root

chdir_plugin_root()


@pytest.mark.parametrize(
    "type_, path",
    [
        pytest.param(
            PackageConfigSource,
            "pkg://some_namespace.namespace_test.dir",
            id="pkg_in_namespace",
        ),
    ],
)
class TestCoreConfigSources(ConfigSourceTestSuite):
    pass


# TODO : ensure that if there is a missing __init__.py file in the dir a proper error is provided
def test_config_in_dir(hydra_global_context: Any) -> None:
    with hydra_global_context(config_dir="../some_namespace/namespace_test/dir"):
        config_loader = GlobalHydra.instance().config_loader()
        assert "cifar10" in config_loader.get_group_options("dataset")
        assert "imagenet" in config_loader.get_group_options("dataset")
        assert "level1" in config_loader.list_groups("")
        assert "level2" in config_loader.list_groups("level1")
        assert "nested1" in config_loader.get_group_options("level1/level2")
        assert "nested2" in config_loader.get_group_options("level1/level2")
