# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional, Type

import pytest

from hydra.plugins.config import ConfigLoadError, ConfigSource, ObjectType


class ConfigSourceTestSuite:
    def test_source_load_config(self, type_: Type[ConfigSource], path: str) -> None:
        src = type_(provider="foo", path=path)

        assert src.load_config(config_path="dataset/imagenet.yaml").config == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }

        assert src.load_config(config_path="dataset/cifar10.yaml").config == {
            "dataset": {"name": "cifar10", "path": "/datasets/cifar10"}
        }

        assert src.load_config(
            config_path="dataset/config_without_extension"
        ).config == {"foo": "bar"}

        assert src.load_config(config_path="config_without_group.yaml").config == {
            "group": False
        }

        with pytest.raises(ConfigLoadError):
            src.load_config(config_path="dataset/not_found.yaml")

    def test_source_file_exists(self, type_: Type[ConfigSource], path: str) -> None:
        src = type_(provider="foo", path=path)

        assert src.exists("dataset/config_without_extension")
        assert src.exists("dataset/imagenet.yaml")
        assert not src.exists("not_there.yaml")

    def test_source_file_type(self, type_: Type[ConfigSource], path: str) -> None:
        src = type_(provider="foo", path=path)

        assert src.get_type("dataset/imagenet.yaml") == ObjectType.CONFIG
        assert src.get_type("dataset/config_without_extension") == ObjectType.CONFIG
        assert src.get_type("dataset") == ObjectType.GROUP
        assert src.get_type("dataset/") == ObjectType.GROUP
        assert src.get_type("not_found") == ObjectType.NOT_FOUND

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
