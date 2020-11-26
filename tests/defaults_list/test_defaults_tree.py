# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re

from pytest import mark, param, raises
from typing import List, Any

from hydra._internal.new_defaults_list import (
    DefaultsTreeNode,
)
from hydra.core.new_default_element import GroupDefault, ConfigDefault
from hydra.core.plugins import Plugins
from hydra.test_utils.test_utils import chdir_hydra_root
from tests.defaults_list import _test_defaults_tree_impl

chdir_hydra_root()

# registers config source plugins
Plugins.instance()

# TODO: test inclusion of nested config item (not group)
# TODO: Test cases where the default lists has package overrides
#   defaults list packages to test : _global_, _global_.foo, _name_


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "empty",
            [],
            DefaultsTreeNode(node=ConfigDefault(path="empty")),
            id="empty",
        ),
        param(
            "config_default",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="config_default"),
                children=[ConfigDefault(path="_self_"), ConfigDefault(path="empty")],
            ),
            id="config_default",
        ),
        param(
            "group_default",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="group_default",
        ),
        param(
            "optional",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="optional"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1", optional=True),
                ],
            ),
            id="optional",
        ),
        param(
            "self_leading",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="self_leading"),
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
                node=ConfigDefault(path="self_trailing"),
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
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file1"),
                        ],
                    ),
                ],
            ),
            id="include_nested_group",
        ),
        param(
            "include_nested_config_item",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_config_item"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="config_item"),
                        children=[
                            ConfigDefault(path="_self_"),
                            ConfigDefault(path="group2/file1"),
                        ],
                    ),
                ],
            ),
            id="include_nested_config_item",
        ),
    ],
)
def test_simple_defaults_tree_cases(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "empty",
            ["+group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="empty"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="empty:append",
        ),
        param(
            "config_default",
            ["+group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="config_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    ConfigDefault(path="empty"),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="config_default:append",
        ),
        param(
            "group_default",
            ["+group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    # config tree allow for duplicate items
                    GroupDefault(group="group1", name="file1"),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="group_default:append",
        ),
        param(
            "self_trailing",
            ["+group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="self_trailing"),
                children=[
                    GroupDefault(group="group1", name="file1"),
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="self_trailing:append",
        ),
        param(
            "include_nested_group",
            ["+group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file1"),
                        ],
                    ),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="include_nested_group:append",
        ),
    ],
)
def test_tree_with_append_override(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "group_default",
            ["group1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2"),
                ],
            ),
            id="group_default:override",
        ),
        param(
            "optional",
            ["group1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="optional"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2", optional=True),
                ],
            ),
            id="optional:override",
        ),
        param(
            "include_nested_group",
            ["group1=group_item2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item2"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file2"),
                        ],
                    ),
                ],
            ),
            id="include_nested_group:override",
        ),
        param(
            "include_nested_group",
            ["group1/group2=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file2"),
                        ],
                    ),
                ],
            ),
            id="include_nested_group:override_nested",
        ),
    ],
)
def test_simple_group_override(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "error_self_pkg1",
            [],
            raises(ValueError, match=re.escape("_self_@PACKAGE is not supported")),
            id="error_self_pkg1",
        ),
    ],
)
def test_errors(
    config_name: str,
    overrides: List[str],
    expected: Any,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "config_default_pkg1",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="config_default_pkg1"),
                children=[
                    ConfigDefault(path="_self_"),
                    ConfigDefault(path="empty", package="pkg1"),
                ],
            ),
            id="config_default_pkg1",
        ),
        param(
            "group_default_pkg1",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_pkg1"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1", package="pkg1"),
                ],
            ),
            id="group_default_pkg1",
        ),
        param(
            "include_nested_group_pkg2",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group_pkg2"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1_pkg2"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file1", package="pkg2"),
                        ],
                    ),
                ],
            ),
            id="include_nested_group_pkg2",
        ),
        param(
            "include_nested_config_item_pkg2",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_config_item_pkg2"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="config_item_pkg2"),
                        children=[
                            ConfigDefault(path="_self_"),
                            ConfigDefault(path="group2/file1", package="pkg2"),
                        ],
                    ),
                ],
            ),
            id="include_nested_config_item_pkg2",
        ),
    ],
)
def test_defaults_tree_with_package_overrides(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )
