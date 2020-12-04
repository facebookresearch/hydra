# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any, List, Optional, Type

import pytest
from pytest import mark, param, raises

from hydra.core import DefaultElement
from hydra.core.object_type import ObjectType
from hydra.errors import HydraException
from hydra.plugins.config_source import ConfigLoadError, ConfigSource


class ConfigSourceTestSuite:
    def skip_overlap_config_path_name(self) -> bool:
        """
        Some config source plugins do not support config name and path overlap.
        For example the following may not be allowed:
        (dataset exists both as a config object and a config group)
        /dateset.yaml
        /dataset/cifar.yaml

        Overriding and returning True here will disable testing of this scenario
        by assuming the dataset config (dataset.yaml) is not present.
        """
        return False

    def test_not_available(self, type_: Type[ConfigSource], path: str) -> None:
        scheme = type_(provider="foo", path=path).scheme()
        # Test is meaningless for StructuredConfigSource
        if scheme == "structured":
            return
        src = type_(provider="foo", path=f"{scheme}://___NOT_FOUND___")
        assert not src.available()

    @mark.parametrize(  # type: ignore
        "config_path, expected",
        [
            pytest.param("", True, id="empty"),
            pytest.param("dataset", True, id="dataset"),
            pytest.param("optimizer", True, id="optimizer"),
            pytest.param(
                "configs_with_defaults_list",
                True,
                id="configs_with_defaults_list",
            ),
            pytest.param("dataset/imagenet", False, id="dataset/imagenet"),
            pytest.param("level1", True, id="level1"),
            pytest.param("level1/level2", True, id="level1/level2"),
            pytest.param("level1/level2/nested1", False, id="level1/level2/nested1"),
            pytest.param("not_found", False, id="not_found"),
        ],
    )
    def test_is_group(
        self, type_: Type[ConfigSource], path: str, config_path: str, expected: bool
    ) -> None:
        src = type_(provider="foo", path=path)
        ret = src.is_group(config_path=config_path)
        assert ret == expected

    @mark.parametrize(  # type: ignore
        "config_path, expected",
        [
            ("", False),
            ("optimizer", False),
            ("dataset/imagenet", True),
            ("dataset/imagenet.yaml", True),
            ("dataset/imagenet.foobar", False),
            ("configs_with_defaults_list/global_package", True),
            ("configs_with_defaults_list/group_package", True),
            ("level1", False),
            ("level1/level2", False),
            ("level1/level2/nested1", True),
            ("not_found", False),
        ],
    )
    def test_is_config(
        self, type_: Type[ConfigSource], path: str, config_path: str, expected: bool
    ) -> None:
        src = type_(provider="foo", path=path)
        ret = src.is_config(config_path=config_path)
        assert ret == expected

    @mark.parametrize(  # type: ignore
        "config_path, expected",
        [
            ("dataset", True),
        ],
    )
    def test_is_config_with_overlap_name(
        self, type_: Type[ConfigSource], path: str, config_path: str, expected: bool
    ) -> None:
        if self.skip_overlap_config_path_name():
            pytest.skip(
                f"ConfigSourcePlugin {type_.__name__} does not support config objects and config groups "
                f"with overlapping names."
            )
        src = type_(provider="foo", path=path)
        ret = src.is_config(config_path=config_path)
        assert ret == expected

    @mark.parametrize(  # type: ignore
        "config_path,results_filter,expected",
        [
            # groups
            ("", ObjectType.GROUP, ["dataset", "level1", "optimizer"]),
            ("dataset", ObjectType.GROUP, []),
            ("optimizer", ObjectType.GROUP, []),
            ("level1", ObjectType.GROUP, ["level2"]),
            ("level1/level2", ObjectType.GROUP, []),
            # Configs
            ("", ObjectType.CONFIG, ["config_without_group"]),
            ("dataset", ObjectType.CONFIG, ["cifar10", "imagenet"]),
            ("optimizer", ObjectType.CONFIG, ["adam", "nesterov"]),
            ("level1", ObjectType.CONFIG, []),
            ("level1/level2", ObjectType.CONFIG, ["nested1", "nested2"]),
            # both
            ("", None, ["config_without_group", "dataset", "level1", "optimizer"]),
            ("dataset", None, ["cifar10", "imagenet"]),
            ("optimizer", None, ["adam", "nesterov"]),
            ("level1", None, ["level2"]),
            ("level1/level2", None, ["nested1", "nested2"]),
            ("", None, ["config_without_group", "dataset", "level1", "optimizer"]),
        ],
    )
    def test_list(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        results_filter: Optional[ObjectType],
        expected: List[str],
    ) -> None:
        src = type_(provider="foo", path=path)
        ret = src.list(config_path=config_path, results_filter=results_filter)
        for x in expected:
            assert x in ret
        assert ret == sorted(ret)

    @mark.parametrize(  # type: ignore
        "config_path,results_filter,expected",
        [
            # Configs
            ("", ObjectType.CONFIG, ["dataset"]),
        ],
    )
    def test_list_with_overlap_name(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        results_filter: Optional[ObjectType],
        expected: List[str],
    ) -> None:
        if self.skip_overlap_config_path_name():
            pytest.skip(
                f"ConfigSourcePlugin {type_.__name__} does not support config objects and config groups "
                f"with overlapping names."
            )
        src = type_(provider="foo", path=path)
        ret = src.list(config_path=config_path, results_filter=results_filter)
        for x in expected:
            assert x in ret
        assert ret == sorted(ret)

    @mark.parametrize(  # type: ignore
        "config_path,expected_config,expected_defaults_list",
        [
            param(
                "config_without_group",
                {"group": False},
                [],
                id="config_without_group",
            ),
            param(
                "config_with_unicode",
                {"group": "数据库"},
                [],
                id="config_with_unicode",
            ),
            param(
                "dataset/imagenet",
                {"dataset": {"name": "imagenet", "path": "/datasets/imagenet"}},
                [],
                id="dataset/imagenet",
            ),
            param(
                "dataset/cifar10",
                {"dataset": {"name": "cifar10", "path": "/datasets/cifar10"}},
                [],
                id="dataset/cifar10",
            ),
            param(
                "dataset/not_found",
                raises(ConfigLoadError),
                [],
                id="dataset/not_found",
            ),
            param(
                "level1/level2/nested1",
                {"l1_l2_n1": True},
                [],
                id="level1/level2/nested1",
            ),
            param(
                "level1/level2/nested2",
                {"l1_l2_n2": True},
                [],
                id="level1/level2/nested2",
            ),
            param(
                "config_with_defaults_list",
                {"key": "value"},
                [
                    DefaultElement(
                        config_group="dataset",
                        config_name="imagenet",
                        parent="config_with_defaults_list",
                    )
                ],
                id="config_with_defaults_list",
            ),
            param(
                "configs_with_defaults_list/global_package",
                {"configs_with_defaults_list": {"x": 10}},
                [
                    DefaultElement(
                        config_group="foo",
                        config_name="bar",
                        parent="configs_with_defaults_list/global_package",
                    )
                ],
                id="configs_with_defaults_list/global_package",
            ),
            param(
                "configs_with_defaults_list/group_package",
                {"configs_with_defaults_list": {"x": 10}},
                [
                    DefaultElement(
                        config_group="foo",
                        config_name="bar",
                        parent="configs_with_defaults_list/group_package",
                    )
                ],
                id="configs_with_defaults_list/group_package",
            ),
        ],
    )
    def test_source_load_config(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        expected_defaults_list: List[DefaultElement],
        expected_config: Any,
        recwarn: Any,
    ) -> None:
        assert issubclass(type_, ConfigSource)
        src = type_(provider="foo", path=path)
        if isinstance(expected_config, dict):
            ret = src.load_config(config_path=config_path, is_primary_config=False)
            assert ret.config == expected_config
            assert ret.defaults_list == expected_defaults_list
        else:
            with expected_config:
                src.load_config(config_path=config_path, is_primary_config=False)

    @mark.parametrize(  # type: ignore
        "config_path, expected_result, expected_package",
        [
            param("package_test/none", {"foo": "bar"}, "", id="none"),
            param(
                "package_test/explicit",
                {"a": {"b": {"foo": "bar"}}},
                "a.b",
                id="explicit",
            ),
            param("package_test/global", {"foo": "bar"}, "", id="global"),
            param(
                "package_test/group",
                {"package_test": {"foo": "bar"}},
                "package_test",
                id="group",
            ),
            param(
                "package_test/group_name",
                {"foo": {"package_test": {"group_name": {"foo": "bar"}}}},
                "foo.package_test.group_name",
                id="group_name",
            ),
            param("package_test/name", {"name": {"foo": "bar"}}, "name", id="name"),
        ],
    )
    def test_package_behavior(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        expected_result: Any,
        expected_package: str,
        recwarn: Any,
    ) -> None:
        src = type_(provider="foo", path=path)
        cfg = src.load_config(config_path=config_path, is_primary_config=False)
        assert cfg.header["package"] == expected_package
        assert cfg.config == expected_result

    def test_default_package_for_primary_config(
        self, type_: Type[ConfigSource], path: str
    ) -> None:
        src = type_(provider="foo", path=path)
        cfg = src.load_config(config_path="primary_config", is_primary_config=True)
        assert cfg.header["package"] == ""

    def test_primary_config_with_non_global_package(
        self, type_: Type[ConfigSource], path: str
    ) -> None:
        src = type_(provider="foo", path=path)
        cfg = src.load_config(
            config_path="primary_config_with_non_global_package",
            is_primary_config=True,
        )
        assert cfg.header["package"] == "foo"

    def test_load_defaults_list(self, type_: Type[ConfigSource], path: str) -> None:
        src = type_(provider="foo", path=path)
        ret = src.load_config(
            config_path="config_with_defaults_list", is_primary_config=True
        )
        assert ret.defaults_list == [
            DefaultElement(
                config_group="dataset",
                config_name="imagenet",
                parent="config_with_defaults_list",
            )
        ]
