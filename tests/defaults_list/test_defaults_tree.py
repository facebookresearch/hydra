# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from textwrap import dedent
from typing import Any, List

from pytest import mark, param, raises

from hydra.core.new_default_element import (
    ConfigDefault,
    GroupDefault,
    VirtualRoot,
    DefaultsTreeNode,
)
from hydra.core.plugins import Plugins
from hydra.errors import ConfigCompositionException
from hydra.test_utils.test_utils import chdir_hydra_root
from tests.defaults_list import _test_defaults_tree_impl

chdir_hydra_root()

# registers config source plugins
Plugins.instance()


@mark.parametrize(  # type: ignore
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


@mark.parametrize(  # type: ignore
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


@mark.parametrize(  # type: ignore
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


@mark.parametrize(  # type: ignore
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


@mark.parametrize(  # type: ignore
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


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "group_default_pkg1",
            ["group1@pkg1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_pkg1"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2", package="pkg1"),
                ],
            ),
            id="option_override:group_default_pkg1",
        ),
        param(
            "group_default_pkg1",
            ["group1@wrong=file2"],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    dedent(
                        """\
                        Could not override 'group1@wrong'. No match in the defaults list.
                        To append to your default list use +group1@wrong=file2"""
                    )
                ),
            ),
            id="option_override:group_default_pkg1:bad_package_in_override",
        ),
        param(
            "include_nested_group_pkg2",
            ["group1/group2@group1.pkg2=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group_pkg2"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1_pkg2"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file2", package="pkg2"),
                        ],
                    ),
                ],
            ),
            id="option_override:include_nested_group_pkg2",
        ),
        param(
            "include_nested_group_pkg2",
            ["group1/group2=file2"],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    dedent(
                        """\
                        Could not override 'group1/group2'. No match in the defaults list.
                        To append to your default list use +group1/group2=file2"""
                    )
                ),
            ),
            id="option_override:include_nested_group_pkg2:missing_package_in_override",
        ),
    ],
)
def test_defaults_tree_with_package_overrides__group_override(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "override_same_level",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_same_level"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2"),
                ],
            ),
            id="override_same_level",
        ),
        param(
            "override_same_level",
            ["group1=file3"],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_same_level"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file3"),
                ],
            ),
            id="override_same_level:external_override",
        ),
        param(
            "include_override_same_level",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_override_same_level"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1",
                            name="override_same_level",
                        ),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(
                                group="group2",
                                name="file2",
                            ),
                        ],
                    ),
                ],
            ),
            id="include_override_same_level",
        ),
        param(
            "include_override_same_level",
            ["group1/group2=file3"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_override_same_level"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1",
                            name="override_same_level",
                        ),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(
                                group="group2",
                                name="file3",
                            ),
                        ],
                    ),
                ],
            ),
            id="include_override_same_level:external_override",
        ),
        param(
            "override_nested_group_item",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_nested_group_item"),
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
            id="override_nested_group_item",
        ),
        param(
            "override_nested_group_item",
            ["group1/group2=file3"],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_nested_group_item"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file3"),
                        ],
                    ),
                ],
            ),
            id="override_nested_group_item:external_override",
        ),
    ],
)
def test_override_option_from_defaults_list(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "two_group_defaults_different_pkgs",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="two_group_defaults_different_pkgs"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1", package="pkg1"),
                    GroupDefault(group="group1", name="file1", package="pkg2"),
                ],
            ),
            id="two_group_defaults_different_pkgs",
        ),
        param(
            "two_group_defaults_different_pkgs",
            ["group1@pkg1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="two_group_defaults_different_pkgs"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2", package="pkg1"),
                    GroupDefault(group="group1", name="file1", package="pkg2"),
                ],
            ),
            id="two_group_defaults_different_pkgs:override_first",
        ),
        param(
            "two_group_defaults_different_pkgs",
            ["group1@pkg2=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="two_group_defaults_different_pkgs"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1", package="pkg1"),
                    GroupDefault(group="group1", name="file2", package="pkg2"),
                ],
            ),
            id="two_group_defaults_different_pkgs:override_second",
        ),
    ],
)
def test_two_group_defaults_different_pkgs(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "empty",
            [],
            DefaultsTreeNode(
                node=VirtualRoot(),
                children=[
                    DefaultsTreeNode(
                        node=ConfigDefault(path="hydra/config"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="help", name="default"),
                            GroupDefault(group="output", name="default"),
                        ],
                    ),
                    ConfigDefault(path="empty"),
                ],
            ),
            id="just_hydra",
        ),
        param(
            "override_hydra",
            [],
            DefaultsTreeNode(
                node=VirtualRoot(),
                children=[
                    DefaultsTreeNode(
                        node=ConfigDefault(path="hydra/config"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="help", name="custom1"),
                            GroupDefault(group="output", name="default"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=ConfigDefault(path="override_hydra"),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="override_hydra",
        ),
        param(
            "override_hydra",
            ["hydra/help=custom2"],
            DefaultsTreeNode(
                node=VirtualRoot(),
                children=[
                    DefaultsTreeNode(
                        node=ConfigDefault(path="hydra/config"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="help", name="custom2"),
                            GroupDefault(group="output", name="default"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=ConfigDefault(path="override_hydra"),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="override_hydra+external",
        ),
    ],
)
def test_legacy_hydra_overrides_from_primary_config(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
    recwarn: Any,  # Testing deprecated behavior
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
        prepend_hydra=True,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "group_default_with_explicit_experiment",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_with_explicit_experiment"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", name="override_config_group"
                        ),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="group_default_with_explicit_experiment",
        ),
        param(
            "group_default_with_explicit_experiment",
            ["group1=file3"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_with_explicit_experiment"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file3"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", name="override_config_group"
                        ),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="group_default_with_explicit_experiment:with_external_override",
        ),
    ],
)
def test_group_default_with_explicit_experiment(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=override_config_group"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", name="override_config_group"
                        ),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="group_default_with_appended_experiment",
        ),
        param(
            "group_default",
            ["group1=file3", "+experiment=override_config_group"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file3"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", name="override_config_group"
                        ),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="group_default_with_appended_experiment:with_external_override",
        ),
    ],
)
def test_group_default_with_appended_experiment(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=include_absolute_config"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", name="include_absolute_config"
                        ),
                        children=[
                            GroupDefault(group="/group1/group2", name="file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                ],
            ),
            id="include_absolute_config",
        ),
        param(
            "group_default",
            ["+experiment=include_absolute_config", "group1/group2=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", name="include_absolute_config"
                        ),
                        children=[
                            GroupDefault(group="/group1/group2", name="file2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                ],
            ),
            id="include_absolute_config:with_external_override",
        ),
    ],
)
def test_experiment_include_absolute_config(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name, input_overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=override_hydra"],
            DefaultsTreeNode(
                node=VirtualRoot(),
                children=[
                    DefaultsTreeNode(
                        node=ConfigDefault(path="hydra/config"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="help", name="custom1"),
                            GroupDefault(group="output", name="default"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=ConfigDefault(path="group_default"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group1", name="file1"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=GroupDefault(group="experiment", name="override_hydra"),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="experiment_overriding_hydra_group",
        ),
        param(
            "group_default",
            ["+experiment=override_hydra", "hydra/help=custom2"],
            DefaultsTreeNode(
                node=VirtualRoot(),
                children=[
                    DefaultsTreeNode(
                        node=ConfigDefault(path="hydra/config"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="help", name="custom2"),
                            GroupDefault(group="output", name="default"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=ConfigDefault(path="group_default"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group1", name="file1"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=GroupDefault(group="experiment", name="override_hydra"),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="experiment_overriding_hydra_group:with_external_hydra_override",
        ),
    ],
)
def test_experiment_overriding_hydra_group(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
        prepend_hydra=True,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "experiment/override_hydra",
            [],
            DefaultsTreeNode(
                node=VirtualRoot(),
                children=[
                    DefaultsTreeNode(
                        node=ConfigDefault(path="hydra/config"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="help", name="custom1"),
                            GroupDefault(group="output", name="default"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=ConfigDefault(path="experiment/override_hydra"),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="experiment_overriding_hydra_group_as_primary",
        ),
    ],
)
def test_experiment_as_primary_config(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
        prepend_hydra=True,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "test_extend_same_group",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="test_extend_same_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", name="here"),
                        children=[
                            ConfigDefault(path="base_db"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                ],
            ),
            id="test_extend_same_group",
        ),
        param(
            "test_extend_from_external_group",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="test_extend_from_external_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", name="external"),
                        children=[
                            ConfigDefault(path="/db/base_db", package=""),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                ],
            ),
            id="test_extend_from_external_group",
        ),
        param(
            "test_extend_from_nested_group",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="test_extend_from_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", name="nested"),
                        children=[
                            ConfigDefault(path="nested/base_db", package=""),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                ],
            ),
            id="test_extend_from_nested_group",
        ),
        param(
            "test_extend_from_nested_group",
            ["extend=nested_here_keyword"],
            DefaultsTreeNode(
                node=ConfigDefault(path="test_extend_from_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", name="nested_here_keyword"),
                        children=[
                            ConfigDefault(path="nested/base_db", package=""),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                ],
            ),
            id="nested_here_keyword",
        ),
    ],
)
def test_extension_use_cases(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "with_missing",
            [],
            raises(
                ConfigCompositionException,
                match=dedent(
                    """\
                You must specify 'db', e.g, db=<OPTION>
                Available options:"""
                ),
            ),
            id="with_missing",
        ),
        param(
            "with_missing",
            ["db=base_db"],
            DefaultsTreeNode(
                node=ConfigDefault(path="with_missing"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="db", name="base_db"),
                ],
            ),
            id="with_missing:override",
        ),
        param(
            "empty",
            ["+group1=with_missing"],
            raises(
                ConfigCompositionException,
                match=dedent(
                    """\
                    You must specify 'group1/group2', e.g, group1/group2=<OPTION>
                    Available options"""
                ),
            ),
            id="nested_missing",
        ),
        param(
            "empty",
            ["+group1=with_missing", "group1/group2=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="empty"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="with_missing"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file1"),
                        ],
                    ),
                ],
            ),
            id="nested_missing:override",
        ),
    ],
)
def test_with_missing(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "with_missing",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="with_missing"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="db", name="???"),
                ],
            ),
            id="with_missing",
        ),
    ],
)
def test_with_missing_and_skip_missing_flag(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
        skip_missing=True,
    )
