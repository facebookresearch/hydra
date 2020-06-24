# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any, List, Optional, Type

from pytest import mark, param, raises

from hydra.core.object_type import ObjectType
from hydra.errors import HydraException
from hydra.plugins.config_source import ConfigLoadError, ConfigSource


class ConfigSourceTestSuite:
    @mark.parametrize(  # type: ignore
        "config_path, expected",
        [
            ("", True),
            ("dataset", True),
            ("optimizer", True),
            ("dataset/imagenet", False),
            ("level1", True),
            ("level1/level2", True),
            ("level1/level2/nested1", False),
            ("not_found", False),
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
            ("dataset", True),
            ("optimizer", False),
            ("dataset/imagenet", True),
            ("dataset/imagenet.yaml", True),
            ("dataset/imagenet.foobar", False),
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
        "config_path,results_filter,expected",
        [
            # groups
            ("", ObjectType.GROUP, ["dataset", "level1", "optimizer"]),
            ("dataset", ObjectType.GROUP, []),
            ("optimizer", ObjectType.GROUP, []),
            ("level1", ObjectType.GROUP, ["level2"],),
            ("level1/level2", ObjectType.GROUP, []),
            # Configs
            ("", ObjectType.CONFIG, ["config_without_group", "dataset"]),
            ("dataset", ObjectType.CONFIG, ["cifar10", "imagenet"],),
            ("optimizer", ObjectType.CONFIG, ["adam", "nesterov"],),
            ("level1", ObjectType.CONFIG, [],),
            ("level1/level2", ObjectType.CONFIG, ["nested1", "nested2"]),
            # both
            ("", None, ["config_without_group", "dataset", "level1", "optimizer"]),
            ("dataset", None, ["cifar10", "imagenet"]),
            ("optimizer", None, ["adam", "nesterov"]),
            ("level1", None, ["level2"],),
            ("level1/level2", None, ["nested1", "nested2"]),
            ("", None, ["config_without_group", "dataset", "level1", "optimizer"]),
            ("dataset", None, ["cifar10", "imagenet"]),
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
        "config_path,expected,expectation",
        [
            param(
                "config_without_group",
                {"group": False},
                None,
                id="config_without_group",
            ),
            param(
                "dataset/imagenet",
                {"dataset": {"name": "imagenet", "path": "/datasets/imagenet"}},
                None,
                id="dataset/imagenet",
            ),
            param(
                "dataset/cifar10",
                {"dataset": {"name": "cifar10", "path": "/datasets/cifar10"}},
                None,
                id="dataset/cifar10",
            ),
            param(
                "dataset/not_found",
                None,
                raises(ConfigLoadError),
                id="dataset/not_found",
            ),
            param(
                "level1/level2/nested1",
                {"l1_l2_n1": True},
                None,
                id="level1/level2/nested1",
            ),
            param(
                "level1/level2/nested2",
                {"l1_l2_n2": True},
                None,
                id="level1/level2/nested2",
            ),
        ],
    )
    def test_source_load_config(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        expected: Any,
        expectation: Any,
        recwarn: Any,
    ) -> None:
        assert issubclass(type_, ConfigSource)
        src = type_(provider="foo", path=path)
        if expectation is not None:
            with expectation:
                src.load_config(config_path=config_path, is_primary_config=False)
        else:
            ret = src.load_config(config_path=config_path, is_primary_config=False)
            assert ret.config == expected

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
        self, type_: Type[ConfigSource], path: str,
    ) -> None:
        src = type_(provider="foo", path=path)
        cfg = src.load_config(config_path="primary_config", is_primary_config=True)
        assert cfg.header["package"] == ""

    def test_primary_config_with_non_global_package_errors(
        self, type_: Type[ConfigSource], path: str,
    ) -> None:
        src = type_(provider="foo", path=path)
        with raises(
            HydraException,
            match=re.escape(
                "Primary config 'primary_config_with_non_global_package' must be in the _global_ package; "
                "effective package : 'foo'"
            ),
        ):
            src.load_config(
                config_path="primary_config_with_non_global_package",
                is_primary_config=True,
            )
