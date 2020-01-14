# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

import pytest

from hydra._internal import ConfigRepository, ConfigSearchPathImpl
from hydra._internal.core_plugins.file_config_source import FileConfigSource
from hydra._internal.core_plugins.package_config_source import PackageConfigSource
from hydra.core.plugins import Plugins
from hydra.plugins.config import ObjectType
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()

Plugins.register_config_sources()


@pytest.mark.parametrize(
    "type_, path",
    [
        (FileConfigSource, "file://tests/test_apps/config_source_test_configs"),
        (PackageConfigSource, "pkg://tests.test_apps.config_source_test_configs"),
    ],
)
class TestCoreConfigSources(ConfigSourceTestSuite):
    pass


def create_config_search_path(path: str) -> ConfigSearchPathImpl:
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path=path)
    return csp


@pytest.mark.parametrize(
    "path",
    [
        "file://tests/test_apps/config_source_test_configs",
        "pkg://tests.test_apps/config_source_test_configs",
    ],
)
class TestConfigRepository:
    def test_config_repository_load(self, path: str) -> None:
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        ret = repo.load_config(config_path="dataset/imagenet.yaml")
        assert ret is not None
        assert ret.config == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }
        assert repo.load_config(config_path="not_found.yaml") is None

    def test_config_repository_exists(self, path: str) -> None:
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        assert repo.exists("dataset/imagenet.yaml")
        assert not repo.exists("not_found.yaml")

    @pytest.mark.parametrize(  # type: ignore
        "config_path,results_filter,expected",
        [
            ("", None, ["config_without_group", "dataset", "optimizer"]),
            ("", ObjectType.GROUP, ["dataset", "optimizer"]),
            ("", ObjectType.CONFIG, ["config_without_group"]),
            ("dataset", None, ["cifar10", "config_without_extension", "imagenet"]),
            ("dataset", ObjectType.GROUP, []),
            (
                "dataset",
                ObjectType.CONFIG,
                ["cifar10", "config_without_extension", "imagenet"],
            ),
        ],
    )
    def test_config_repository_list(
        self,
        path: str,
        config_path: str,
        results_filter: Optional[ObjectType],
        expected: List[str],
    ) -> None:
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        ret = repo.get_group_options(
            group_name=config_path, results_filter=results_filter
        )
        assert ret == expected
