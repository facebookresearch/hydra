# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional, Type

import pytest

from hydra._internal.config import (
    ConfigRepository,
    ConfigSource,
    FileConfigSource,
    ObjectType,
    PackageConfigSource,
)
from hydra._internal.config_search_path import ConfigSearchPath
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


@pytest.mark.parametrize(
    "type_, path",
    [
        (FileConfigSource, "file://tests/test_apps/app_with_cfg_groups/conf"),
        (PackageConfigSource, "pkg://tests.test_apps.app_with_cfg_groups.conf"),
    ],
)
class TestConfigSource:
    def test_source_load_config(self, type_: Type[ConfigSource], path: str) -> None:
        src = type_(provider="foo", path=path)

        ret = src.load_config(config_path="dataset/imagenet.yaml")
        assert ret.config == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }

        with pytest.raises(IOError):
            src.load_config(config_path="dataset/not_found.yaml")

    def test_source_file_exists(self, type_: Type[ConfigSource], path: str) -> None:
        src = type_(provider="foo", path=path)

        assert src.exists("dataset/imagenet.yaml")
        assert not src.exists("not_there.yaml")

    def test_source_file_type(self, type_: Type[ConfigSource], path: str) -> None:
        src = type_(provider="foo", path=path)

        assert src.get_type("dataset/imagenet.yaml") == ObjectType.CONFIG
        assert src.get_type("dataset") == ObjectType.GROUP
        assert src.get_type("dataset/") == ObjectType.GROUP
        assert src.get_type("not_found") == ObjectType.NOT_FOUND

    @pytest.mark.parametrize(  # type: ignore
        "config_path,results_filter,expected",
        [
            ("", None, ["config", "dataset", "optimizer"]),
            ("", ObjectType.GROUP, ["dataset", "optimizer"]),
            ("", ObjectType.CONFIG, ["config"]),
            ("dataset", None, ["imagenet", "nesterov"]),
            ("dataset", ObjectType.GROUP, []),
            ("dataset", ObjectType.CONFIG, ["imagenet", "nesterov"]),
        ],
    )
    def test_source_list(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        results_filter: Optional[ObjectType],
        expected: List[str],
    ) -> None:
        src = type_(provider="foo", path=path)
        ret = src.list(config_path=config_path, results_filter=results_filter)
        assert ret == expected


def create_config_search_path(path: str) -> ConfigSearchPath:
    csp = ConfigSearchPath()
    csp.append(provider="test", path=path)
    return csp


@pytest.mark.parametrize(
    "path",
    [
        "file://tests/test_apps/app_with_cfg_groups/conf",
        "pkg://tests.test_apps.app_with_cfg_groups.conf",
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
            ("", None, ["config", "dataset", "optimizer"]),
            ("", ObjectType.GROUP, ["dataset", "optimizer"]),
            ("", ObjectType.CONFIG, ["config"]),
            ("dataset", None, ["imagenet", "nesterov"]),
            ("dataset", ObjectType.GROUP, []),
            ("dataset", ObjectType.CONFIG, ["imagenet", "nesterov"]),
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
