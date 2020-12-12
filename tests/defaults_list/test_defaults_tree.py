# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from textwrap import dedent
from typing import Any, List, Optional

from pytest import mark, param, raises, warns

from hydra.core.default_element import (
    ConfigDefault,
    DefaultsTreeNode,
    GroupDefault,
    VirtualRoot,
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
            ["+group2=file1"],
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
                    GroupDefault(group="group2", name="file1"),
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
                        Could not override 'group1@wrong'.
                        Did you mean to override group1@pkg1?
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
                        Could not override 'group1/group2'.
                        Did you mean to override group1/group2@group1.pkg2?
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
        param(
            "override_wrong_order",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    dedent(
                        """\
                        In override_wrong_order: Override 'group1 : file2' is defined before 'group1: file1'.
                        Overrides must be at the end of the defaults list"""
                    )
                ),
            ),
            id="test_override_wrong_order_in_defaults_list",
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
            "legacy_override_hydra",
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
                        node=ConfigDefault(path="legacy_override_hydra"),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="legacy_override_hydra",
        ),
        param(
            "legacy_override_hydra",
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
                        node=ConfigDefault(path="legacy_override_hydra"),
                        children=[ConfigDefault(path="_self_")],
                    ),
                ],
            ),
            id="legacy_override_hydra+external",
        ),
    ],
)
def test_legacy_hydra_overrides_from_primary_config(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    msg = dedent(
        """\
        Invalid overriding of hydra/help:
        Default list overrides requires 'override: true'.
        See https://hydra.cc/docs/next/upgrades/1.0_to_1.1/default_list_override for more information."""
    )
    with warns(expected_warning=UserWarning, match=re.escape(msg)):
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
                    GroupDefault(group="experiment", name="override_config_group"),
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
                    GroupDefault(group="experiment", name="override_config_group"),
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
                    GroupDefault(group="experiment", name="override_config_group"),
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
                    GroupDefault(group="experiment", name="override_config_group"),
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
                    GroupDefault(group="experiment", name="override_hydra"),
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
                    GroupDefault(group="experiment", name="override_hydra"),
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
                    ConfigDefault(path="experiment/override_hydra"),
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


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "placeholder",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="placeholder"),
                children=[ConfigDefault(path="_self_"), GroupDefault(group="group1")],
            ),
            id="placeholder",
        ),
        param(
            "placeholder",
            ["group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="placeholder"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="placeholder:override",
        ),
        param(
            "nested_placeholder",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="nested_placeholder"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="placeholder"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2"),
                        ],
                    ),
                ],
            ),
            id="nested_placeholder",
        ),
        param(
            "nested_placeholder",
            ["group1/group2=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="nested_placeholder"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="placeholder"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file1"),
                        ],
                    ),
                ],
            ),
            id="nested_placeholder:override",
        ),
    ],
)
def test_placeholder(
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
            "interpolation_simple",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_simple"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                    GroupDefault(group="group2", name="file2"),
                    GroupDefault(group="group1_group2", name="file1_file2"),
                ],
            ),
            id="interpolation_simple",
        ),
        param(
            "interpolation_simple",
            ["group1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_simple"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2"),
                    GroupDefault(group="group2", name="file2"),
                    GroupDefault(group="group1_group2", name="file2_file2"),
                ],
            ),
            id="interpolation_simple:override",
        ),
        param(
            "interpolation_forward",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_forward"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1_group2", name="file1_file2"),
                    GroupDefault(group="group1", name="file1"),
                    GroupDefault(group="group2", name="file2"),
                ],
            ),
            id="interpolation_forward",
        ),
        param(
            "interpolation_forward",
            ["group1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_forward"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1_group2", name="file2_file2"),
                    GroupDefault(group="group1", name="file2"),
                    GroupDefault(group="group2", name="file2"),
                ],
            ),
            id="interpolation_forward:override",
        ),
        param(
            "interpolation_nested",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_nested"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1/group2", name="file1"),
                    GroupDefault(group="group1_group2", name="foo_file1"),
                ],
            ),
            id="interpolation_nested",
        ),
        param(
            "interpolation_nested",
            ["group1/group2=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_nested"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1/group2", name="file2"),
                    GroupDefault(group="group1_group2", name="foo_file2"),
                ],
            ),
            id="interpolation_nested:override",
        ),
        param(
            "interpolation_with_package_override",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_with_package_override"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1", package="package"),
                    GroupDefault(group="group2", name="file2"),
                    GroupDefault(group="group1_group2", name="file1_file2"),
                ],
            ),
            id="interpolation_with_package_override",
        ),
        param(
            "interpolation_with_package_override",
            ["group1@package=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_with_package_override"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file2", package="package"),
                    GroupDefault(group="group2", name="file2"),
                    GroupDefault(group="group1_group2", name="file2_file2"),
                ],
            ),
            id="interpolation_with_package_override:override",
        ),
        param(
            "interpolation_with_nested_defaults_list",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_with_nested_defaults_list"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                    GroupDefault(group="group2", name="file1"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1_group2", name="file1_file1_with_defaults_list"
                        ),
                        children=[
                            ConfigDefault(path="_self_"),
                            ConfigDefault(path="empty1"),
                        ],
                    ),
                ],
            ),
            id="interpolation_with_nested_defaults_list",
        ),
        param(
            "interpolation_with_nested_defaults_list",
            ["group2=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_with_nested_defaults_list"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                    GroupDefault(group="group2", name="file2"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1_group2", name="file1_file2_with_defaults_list"
                        ),
                        children=[
                            ConfigDefault(path="_self_"),
                            ConfigDefault(path="empty2"),
                        ],
                    ),
                ],
            ),
            id="interpolation_with_nested_defaults_list:override",
        ),
        param(
            "interpolation_with_nested_defaults_list_with_override",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "group1_group2/file1_file1_defaults_with_override: Overrides are not allowed in the subtree"
                    " of an in interpolated config group (group1_group2/foo=bar)"
                ),
            ),
            id="interpolation_with_nested_defaults_list_with_override",
        ),
    ],
)
def test_interpolation(
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
            "interpolation_legacy_with_self",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_legacy_with_self"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                    GroupDefault(group="group2", name="file2"),
                    GroupDefault(group="group1_group2", name="file1_file2"),
                ],
            ),
            id="interpolation_legacy_with_self",
        ),
        param(
            "interpolation_legacy_without_self",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_legacy_without_self"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1"),
                    GroupDefault(group="group2", name="file2"),
                    GroupDefault(group="group1_group2", name="file1_file2"),
                ],
            ),
            id="interpolation_legacy_without_self",
        ),
    ],
)
def test_legacy_interpolation(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    msg = dedent(
        """
    Defaults list element '.*=.*' is using a deprecated interpolation form.
    See http://hydra.cc/docs/next/upgrades/1.0_to_1.1/defaults_list_interpolation for migration information."""
    )
    with warns(expected_warning=UserWarning, match=msg):
        _test_defaults_tree_impl(
            config_name=config_name,
            input_overrides=overrides,
            expected=expected,
        )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "override_nested_to_null",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_nested_to_null"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2"),
                        ],
                    ),
                ],
            ),
            id="override_nested_to_null",
        ),
        param(
            "override_nested_to_null",
            ["group1/group2=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_nested_to_null"),
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
            id="override_nested_to_null:override",
        ),
    ],
)
def test_override_nested_to_null(
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
            id="delete:include_nested_group:baseline",
        ),
        param(
            "include_nested_group",
            ["~group1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="group_item1", deleted=True),
                ],
            ),
            id="delete:include_nested_group:group1",
        ),
        param(
            "include_nested_group",
            ["~group1/group2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", name="group_item1"),
                        children=[
                            ConfigDefault(path="_self_"),
                            GroupDefault(group="group2", name="file1", deleted=True),
                        ],
                    ),
                ],
            ),
            id="delete:include_nested_group:group1/group2",
        ),
        param(
            "include_nested_group",
            ["~group1=group_item1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="group_item1", deleted=True),
                ],
            ),
            id="delete:include_nested_group:group1=group_item1",
        ),
        param(
            "include_nested_group",
            ["~group1=wrong"],
            raises(
                ConfigCompositionException,
                match="Could not delete 'group1=wrong'. No match in the defaults list",
            ),
            id="delete:include_nested_group:group1=wrong",
        ),
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
            id="delete:two_group_defaults_different_pkgs:baseline",
        ),
        param(
            "two_group_defaults_different_pkgs",
            ["~group1@pkg1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="two_group_defaults_different_pkgs"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(
                        group="group1", name="file1", package="pkg1", deleted=True
                    ),
                    GroupDefault(group="group1", name="file1", package="pkg2"),
                ],
            ),
            id="delete:two_group_defaults_different_pkgs:delete_pkg1",
        ),
        param(
            "two_group_defaults_different_pkgs",
            ["~group1@pkg2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="two_group_defaults_different_pkgs"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file1", package="pkg1"),
                    GroupDefault(
                        group="group1", name="file1", package="pkg2", deleted=True
                    ),
                ],
            ),
            id="delete:two_group_defaults_different_pkgs:delete_pkg1",
        ),
    ],
)
def test_deletion(
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
            "empty",
            ["~group1"],
            raises(
                ConfigCompositionException,
                match="Could not delete 'group1'. No match in the defaults list",
            ),
            id="override_non_existing",
        ),
        param(
            "empty",
            ["~group1=abc"],
            raises(
                ConfigCompositionException,
                match="Could not delete 'group1=abc'. No match in the defaults list",
            ),
            id="override_non_existing",
        ),
        param(
            "empty",
            ["~group1@pkg1=abc"],
            raises(
                ConfigCompositionException,
                match="Could not delete 'group1@pkg1=abc'. No match in the defaults list",
            ),
            id="override_non_existing",
        ),
    ],
)
def test_delete_non_existing(
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
            "duplicate_self",
            [],
            raises(
                ConfigCompositionException,
                match="Duplicate _self_ defined in duplicate_self",
            ),
            id="duplicate_self",
        ),
    ],
)
def test_duplicate_self_error(
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
            "not_found",
            [],
            raises(
                ConfigCompositionException,
                match="^Could not load 'not_found'.*",
            ),
            id="missing_primary",
        ),
        param(
            "empty",
            ["+group1=not_found"],
            raises(
                ConfigCompositionException,
                match="^In 'empty': Could not find 'group1/not_found'\n\nAvailable options in 'group1':",
            ),
            id="missing_included_config",
        ),
        param(
            "empty",
            ["+group1=not_found"],
            raises(
                ConfigCompositionException,
                match="^In 'empty': Could not find 'group1/not_found'\n\nAvailable options in 'group1':",
            ),
            id="missing_included_config",
        ),
    ],
)
def test_missing_config_errors(
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
            "empty",
            ["group1=file1"],
            raises(
                ConfigCompositionException,
                match="Could not override 'group1'. No match in the defaults list.",
            ),
            id="override_non_existing",
        ),
        param(
            "empty",
            ["group1@pkg1=file1"],
            raises(
                ConfigCompositionException,
                match="Could not override 'group1@pkg1'. No match in the defaults list.",
            ),
            id="override_non_existing",
        ),
        param(
            "empty",
            ["group1/group2=file1"],
            raises(
                ConfigCompositionException,
                match="Could not override 'group1/group2'. No match in the defaults list.",
            ),
            id="override_non_existing",
        ),
        param(
            "error_invalid_override",
            [],
            raises(
                ConfigCompositionException,
                match="Could not override 'group1'. No match in the defaults list.",
            ),
            id="error_invalid_override",
        ),
        param(
            "group_default",
            ["group1@foo=file1"],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    dedent(
                        """\
                Could not override 'group1@foo'.
                Did you mean to override group1?
                To append to your default list use +group1@foo=file1"""
                    )
                ),
            ),
            id="no_match_package_one_candidate",
        ),
        param(
            "two_group_defaults_different_pkgs",
            ["group1@foo=file1"],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    dedent(
                        """\
                        Could not override 'group1@foo'.
                        Did you mean to override one of group1@pkg1, group1@pkg2?
                        To append to your default list use +group1@foo=file1"""
                    )
                ),
            ),
            id="no_match_package_multiple_candidates",
        ),
    ],
)
def test_override_errors(
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
            "error_changing_group",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "Multiple values for group1 (file2, file1). To override a value use 'override: true'"
                ),
            ),
            id="error_changing_group",
        ),
    ],
)
def test_error_changing_group_choice(
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
            "missing_optional_default",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="missing_optional_default"),
                children=[
                    ConfigDefault(path="_self_"),
                    ConfigDefault(path="empty"),
                    GroupDefault(
                        group="foo", name="missing", optional=True, deleted=True
                    ),
                ],
            ),
            id="missing_optional_default",
        ),
    ],
)
def test_load_missing_optional(
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
            "group_default_global",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_global"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file_with_global_header"),
                ],
            ),
            id="group_default_global",
        ),
        param(
            "group_default_global",
            ["group1=file_with_global_header"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_global"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", name="file_with_global_header"),
                ],
            ),
            id="group_default_global",
        ),
    ],
)
def test_overriding_group_file_with_global_header(
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
            None,
            [],
            DefaultsTreeNode(node=VirtualRoot()),
            id="none_config",
        ),
        param(
            None,
            ["+group1=file1"],
            DefaultsTreeNode(
                node=VirtualRoot(),
                children=[GroupDefault(group="group1", name="file1")],
            ),
            id="none_config+group1=file1",
        ),
    ],
)
def test_none_config(
    config_name: Optional[str],
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
            None,
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
                    VirtualRoot(),
                ],
            ),
            id="none_config",
        ),
        param(
            None,
            ["+group1=file1"],
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
                    VirtualRoot(),
                    GroupDefault(group="group1", name="file1"),
                ],
            ),
            id="none_config+group1=file1",
        ),
    ],
)
def test_none_config_with_hydra(
    config_name: Optional[str],
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
            "defaults_with_override_only",
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
                    ConfigDefault(path="defaults_with_override_only"),
                ],
            ),
            id="defaults_with_override_only",
        ),
    ],
)
def test_defaults_with_overrides_only(
    config_name: Optional[str],
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
        prepend_hydra=True,
    )
