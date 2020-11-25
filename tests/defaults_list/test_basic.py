# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import mark, param
from typing import List

from hydra._internal.new_defaults_list import (
    create_defaults_list,
    ResultDefault,
)
from hydra.core.new_default_element import InputDefault, GroupDefault, ConfigDefault
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.test_utils.test_utils import chdir_hydra_root
from tests.defaults_list import create_repo

chdir_hydra_root()

# registers config source plugins
Plugins.instance()


# TODO:
#  - (Y) test with simple config group overrides
#  - test with config group overrides overriding config groups @pkg
#  - test handling missing configs mentioned in defaults list (with and without optional)
#  - test overriding configs in absolute location
#  - test duplicate _self_ error
#  - test duplicates in result config list


@mark.parametrize(
    "config_path,expected_list",
    [
        param("empty", [], id="empty"),
        param(
            "group_default",
            [GroupDefault(group="group1", name="file1")],
            id="one_item",
        ),
        param(
            "group_default",
            [GroupDefault(group="group1", name="file1")],
            id="one_item",
        ),
        param(
            "self_leading",
            [
                ConfigDefault(path="_self_"),
                GroupDefault(group="group1", name="file1"),
            ],
            id="self_leading",
        ),
        param(
            "self_trailing",
            [
                GroupDefault(group="group1", name="file1"),
                ConfigDefault(path="_self_"),
            ],
            id="self_trailing",
        ),
        param(
            "optional",
            [
                GroupDefault(group="group1", name="file1", optional=True),
            ],
            id="optional",
        ),
        param(
            "config_default",
            [
                ConfigDefault(path="empty"),
            ],
            id="non_config_group_default",
        ),
    ],
)
def test_loaded_defaults_list(config_path: str, expected_list: List[InputDefault]):
    repo = create_repo()
    result = repo.load_config(config_path=config_path, is_primary_config=True)
    assert result.new_defaults_list == expected_list


def _test_defaults_list_impl(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
) -> None:
    parser = OverridesParser.create()
    repo = create_repo()
    overrides_list = parser.parse_overrides(overrides=overrides)
    result = create_defaults_list(
        repo=repo,
        config_name=config_name,
        overrides_list=overrides_list,
    )

    assert result.defaults == expected


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "empty",
            [],
            [ResultDefault(config_path="empty")],
            id="empty",
        ),
        param(
            "config_default",
            [],
            [
                ResultDefault(config_path="config_default", is_self=True),
                ResultDefault(config_path="empty", parent="config_default"),
            ],
            id="config_default",
        ),
        param(
            "group_default",
            [],
            [
                ResultDefault(config_path="group_default", is_self=True),
                ResultDefault(config_path="group1/file1", parent="group_default"),
            ],
            id="group_default",
        ),
        param(
            "self_leading",
            [],
            [
                ResultDefault(config_path="self_leading", is_self=True),
                ResultDefault(config_path="group1/file1", parent="self_leading"),
            ],
            id="self_leading",
        ),
        param(
            "self_trailing",
            [],
            [
                ResultDefault(config_path="group1/file1", parent="self_trailing"),
                ResultDefault(config_path="self_trailing", is_self=True),
            ],
            id="self_trailing",
        ),
        param(
            "include_nested_group",
            [],
            [
                ResultDefault(config_path="include_nested_group", is_self=True),
                ResultDefault(
                    config_path="group1/group_item1",
                    parent="include_nested_group",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1", parent="group1/group_item1"
                ),
            ],
            id="include_nested_group",
        ),
    ],
)
def test_simple_defaults_list_cases(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(
    "default,expected_group_path,expected_config_path",
    [
        param(
            ConfigDefault(path="bar", parent_base_dir=""),
            "",
            "bar",
            id="config_default:empty_basedir",
        ),
        param(
            ConfigDefault(path="bar", parent_base_dir="foo"),
            "foo",
            "foo/bar",
            id="config_default:with_parent_basedir",
        ),
        param(
            GroupDefault(group="foo", name="bar", parent_base_dir=""),
            "foo",
            "foo/bar",
            id="group_default:empty_basedir",
        ),
        param(
            GroupDefault(group="foo", name="bar", parent_base_dir="zoo"),
            "zoo/foo",
            "zoo/foo/bar",
            id="group_default:with_parent_basedir",
        ),
    ],
)
def test_get_paths(
    default: InputDefault, expected_group_path, expected_config_path
) -> None:
    assert default.get_group_path() == expected_group_path
    assert default.get_config_path() == expected_config_path
