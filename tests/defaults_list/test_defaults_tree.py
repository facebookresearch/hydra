# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import mark, param
from typing import List

from hydra._internal.new_defaults_list import (
    DefaultsTreeNode,
)
from hydra.core.NewDefaultElement import GroupDefault, ConfigDefault
from hydra.core.plugins import Plugins
from hydra.test_utils.test_utils import chdir_hydra_root
from tests.defaults_list import _test_defaults_tree_impl

chdir_hydra_root()

# registers config source plugins
Plugins.instance()


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
            "config_default",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="config_default"),
                children=[ConfigDefault(path="empty")],
            ),
            id="config_default",
        ),
        param(
            "group_default",
            [],
            DefaultsTreeNode(
                parent=ConfigDefault(path="group_default"),
                children=[GroupDefault(group="group1", name="file1")],
            ),
            id="group_default",
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
        config_name=config_name, overrides_list=overrides, expected=expected
    )


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "empty",
            ["+group1=file1"],
            DefaultsTreeNode(
                parent=ConfigDefault(path="empty"),
                children=[GroupDefault(group="group1", name="file1")],
            ),
            id="empty:append",
        ),
        param(
            "config_default",
            ["+group1=file1"],
            DefaultsTreeNode(
                parent=ConfigDefault(path="config_default"),
                children=[
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
                parent=ConfigDefault(path="group_default"),
                children=[
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
                parent=ConfigDefault(path="self_trailing"),
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
                parent=ConfigDefault(path="include_nested_group"),
                children=[
                    DefaultsTreeNode(
                        parent=GroupDefault(group="group1", name="group_item"),
                        children=[GroupDefault(group="group2", name="file1")],
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
        config_name=config_name, overrides_list=overrides, expected=expected
    )
