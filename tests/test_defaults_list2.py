# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import mark, param
from typing import List

from hydra._internal.config_repository import ConfigRepository, IConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.new_defaults_list import (
    create_defaults_list,
    ResultDefault,
    DefaultsTreeNode,
    _create_defaults_tree,
    _create_group_overrides,
)
from hydra.core.NewDefaultElement import InputDefault, GroupDefault, ConfigDefault
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()

# registers config source plugins
Plugins.instance()


# TODO:
#  - test with simple config group overrides
#  - test with config group overrides overriding config groups @pkg
#  - test handling missing configs mentioned in defaults list (with and without optional)
#  - test overriding configs in absolute location


def create_repo() -> IConfigRepository:
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/default_lists")
    return ConfigRepository(config_search_path=csp)


@mark.parametrize(
    "config_path,expected_list",
    [
        param("empty", [], id="empty"),
        param(
            "one_item",
            [GroupDefault(group="group1", name="file1")],
            id="one_item",
        ),
        param(
            "one_item",
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
            "non_config_group_default",
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
    result = create_defaults_list(
        repo=repo,
        config_name=config_name,
        overrides=parser.parse_overrides(overrides=overrides),
    )

    assert result.defaults == expected


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param("empty", [], [], id="empty"),
    ],
)
def test_simple_cases(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


def _test_defaults_tree_impl(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    parser = OverridesParser.create()
    repo = create_repo()
    parent = ConfigDefault(path=config_name)
    root = DefaultsTreeNode(parent=parent)
    group_overrides = _create_group_overrides(
        parser.parse_overrides(overrides=overrides)
    )
    result = _create_defaults_tree(
        repo=repo,
        root=root,
        group_overrides=group_overrides,
        is_primary_config=True,
    )

    assert result == expected


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "empty",
            [],
            DefaultsTreeNode(parent=ConfigDefault(path="empty")),
            id="empty",
        ),
        param(
            "non_config_group_default",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="non_config_group_default"),
                children=[ConfigDefault(path="empty")],
            ),
            id="non_config_group_default",
        ),
        param(
            "one_item",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="one_item"),
                children=[GroupDefault(group="group1", name="file1")],
            ),
            id="one_item",
        ),
        param(
            "optional",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="optional"),
                children=[
                    GroupDefault(group="group1", name="file1", optional=True),
                ],
            ),
            id="optional",
        ),
        param(
            "self_leading",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="self_leading"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="self_leading",
        ),
        param(
            "self_trailing",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="self_trailing"),
                children=[
                    GroupDefault(group="group1", name="file1"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="self_trailing",
        ),
        param(
            "include_nested_group",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="include_nested_group"),
                children=[
                    DefaultsTreeNode(
                        parent=GroupDefault(group="group1", name="group_item"),
                        children=[GroupDefault(group="group2", name="file1")],
                    )
                ],
            ),
            id="include_nested_group",
        ),
    ],
)
def test_simple_defaults_tree_cases(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
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
