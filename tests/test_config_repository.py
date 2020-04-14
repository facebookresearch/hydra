# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, List, Optional

import pytest

from hydra._internal.config_repository import ConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.core_plugins.file_config_source import FileConfigSource
from hydra._internal.core_plugins.package_config_source import PackageConfigSource
from hydra._internal.core_plugins.structured_config_source import StructuredConfigSource
from hydra.core.object_type import ObjectType
from hydra.core.plugins import Plugins
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


@pytest.mark.parametrize(
    "type_, path",
    [
        pytest.param(
            FileConfigSource,
            "file://tests/test_apps/config_source_test/dir",
            id="file://",
        ),
        pytest.param(
            PackageConfigSource,
            "pkg://tests.test_apps.config_source_test.dir",
            id="pkg://",
        ),
        pytest.param(
            StructuredConfigSource,
            "structured://tests.test_apps.config_source_test.structured",
            id="structured://",
        ),
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
        "file://tests/test_apps/config_source_test/dir",
        "pkg://tests.test_apps.config_source_test.dir",
    ],
)
class TestConfigRepository:
    def test_config_repository_load(self, restore_singletons: Any, path: str) -> None:
        Plugins.instance()  # initializes
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        ret = repo.load_config(config_path="dataset/imagenet.yaml")
        assert ret is not None
        assert ret.config == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }
        assert repo.load_config(config_path="not_found.yaml") is None

    def test_config_repository_exists(self, restore_singletons: Any, path: str) -> None:
        Plugins.instance()  # initializes
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        assert repo.exists("dataset/imagenet.yaml")
        assert not repo.exists("not_found.yaml")

    @pytest.mark.parametrize(  # type: ignore
        "config_path,results_filter,expected",
        [
            ("", None, ["config_without_group", "dataset", "level1", "optimizer"]),
            ("", ObjectType.GROUP, ["dataset", "level1", "optimizer"]),
            ("", ObjectType.CONFIG, ["config_without_group", "dataset"]),
            ("dataset", None, ["cifar10", "imagenet"]),
            ("dataset", ObjectType.GROUP, []),
            ("dataset", ObjectType.CONFIG, ["cifar10", "imagenet"]),
            ("level1", ObjectType.GROUP, ["level2"]),
            ("level1", ObjectType.CONFIG, []),
            ("level1/level2", ObjectType.CONFIG, ["nested1", "nested2"]),
        ],
    )
    def test_config_repository_list(
        self,
        restore_singletons: Any,
        path: str,
        config_path: str,
        results_filter: Optional[ObjectType],
        expected: List[str],
    ) -> None:
        Plugins.instance()  # initializes
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        ret = repo.get_group_options(
            group_name=config_path, results_filter=results_filter
        )
        assert ret == expected
