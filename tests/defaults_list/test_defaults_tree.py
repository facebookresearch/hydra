# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from textwrap import dedent
from typing import Any, Dict, List, Optional

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
                children=[ConfigDefault(path="empty"), ConfigDefault(path="_self_")],
            ),
            id="config_default",
        ),
        param(
            "group_default",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1", optional=True),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1"),
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
                    GroupDefault(group="group1", value="file1"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="config_item"),
                        children=[
                            ConfigDefault(path="group2/file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1"),
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
                    ConfigDefault(path="empty"),
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", value="file1"),
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
                    # config tree allow for duplicate items
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", value="file1"),
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
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", value="file1"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group2", value="file1"),
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
                    GroupDefault(group="group1", value="file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file2", optional=True),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item2"),
                        children=[
                            GroupDefault(group="group2", value="file2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
        param(
            "error_changing_group",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "Multiple values for group1. To override a value use 'override group1: file2'"
                ),
            ),
            id="error_changing_group",
        ),
        param(
            "duplicate_self",
            [],
            raises(
                ConfigCompositionException,
                match="Duplicate _self_ defined in duplicate_self",
            ),
            id="duplicate_self",
        ),
        param(
            "invalid_override_in_defaults",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "In 'invalid_override_in_defaults': Could not override 'foo'. No match in the defaults list."
                )
                + "$",
            ),
            id="invalid_override_in_defaults",
        ),
    ],
)
def test_misc_errors(
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
                    ConfigDefault(path="empty", package="pkg1"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1", package="pkg1"),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1_pkg2"),
                        children=[
                            GroupDefault(group="group2", value="file1", package="pkg2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="config_item_pkg2"),
                        children=[
                            ConfigDefault(path="group2/file1", package="pkg2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "group_default_pkg1",
            ["group1@pkg1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_pkg1"),
                children=[
                    GroupDefault(group="group1", value="file2", package="pkg1"),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1_pkg2"),
                        children=[
                            GroupDefault(group="group2", value="file2", package="pkg2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "override_same_level",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_same_level"),
                children=[
                    GroupDefault(group="group1", value="file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file3"),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1",
                            value="override_same_level",
                        ),
                        children=[
                            GroupDefault(
                                group="group2",
                                value="file2",
                            ),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1",
                            value="override_same_level",
                        ),
                        children=[
                            GroupDefault(
                                group="group2",
                                value="file3",
                            ),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file3"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "two_group_defaults_different_pkgs",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="two_group_defaults_different_pkgs"),
                children=[
                    GroupDefault(group="group1", value="file1", package="pkg1"),
                    GroupDefault(group="group1", value="file1", package="pkg2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file2", package="pkg1"),
                    GroupDefault(group="group1", value="file1", package="pkg2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1", package="pkg1"),
                    GroupDefault(group="group1", value="file2", package="pkg2"),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
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
                            GroupDefault(group="help", value="custom1"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
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
                            GroupDefault(group="help", value="custom2"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
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
        Default list overrides requires 'override' keyword.
        See https://hydra.cc/docs/next/upgrades/1.0_to_1.1/defaults_list_override for more information."""
    )
    with warns(expected_warning=UserWarning, match=re.escape(msg)):
        _test_defaults_tree_impl(
            config_name=config_name,
            input_overrides=overrides,
            expected=expected,
            prepend_hydra=True,
        )


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "group_default_with_explicit_experiment",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_with_explicit_experiment"),
                children=[
                    GroupDefault(group="group1", value="file2"),
                    GroupDefault(group="experiment", value="override_config_group"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file3"),
                    GroupDefault(group="experiment", value="override_config_group"),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=override_config_group"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    GroupDefault(group="group1", value="file2"),
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="experiment", value="override_config_group"),
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
                    GroupDefault(group="group1", value="file3"),
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="experiment", value="override_config_group"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=include_absolute_config"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", value="include_absolute_config"
                        ),
                        children=[
                            GroupDefault(group="/group1/group2", value="file1"),
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
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="experiment", value="include_absolute_config"
                        ),
                        children=[
                            GroupDefault(group="/group1/group2", value="file2"),
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


@mark.parametrize(
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
                            GroupDefault(group="help", value="custom1"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=ConfigDefault(path="group_default"),
                        children=[
                            GroupDefault(group="group1", value="file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    GroupDefault(group="experiment", value="override_hydra"),
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
                            GroupDefault(group="help", value="custom2"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    DefaultsTreeNode(
                        node=ConfigDefault(path="group_default"),
                        children=[
                            GroupDefault(group="group1", value="file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    GroupDefault(group="experiment", value="override_hydra"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=override_with_global_default"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    GroupDefault(group="group1", value="file2"),
                    ConfigDefault(path="_self_"),
                    GroupDefault(
                        group="experiment", value="override_with_global_default"
                    ),
                ],
            ),
            id="include_absolute_config:override_with_global_default",
        ),
    ],
)
def test_experiment_overriding_global_group(
    config_name: str,
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
        prepend_hydra=False,
    )


@mark.parametrize(
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
                            GroupDefault(group="help", value="custom1"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "test_extend_same_group",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="test_extend_same_group"),
                children=[
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", value="here"),
                        children=[
                            ConfigDefault(path="base_db"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", value="external"),
                        children=[
                            ConfigDefault(path="/db/base_db", package=""),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", value="nested"),
                        children=[
                            ConfigDefault(path="nested/base_db", package=""),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="extend", value="nested_here_keyword"),
                        children=[
                            ConfigDefault(path="nested/base_db", package=""),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
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
                    GroupDefault(group="db", value="base_db"),
                    ConfigDefault(path="_self_"),
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
                        node=GroupDefault(group="group1", value="with_missing"),
                        children=[
                            GroupDefault(group="group2", value="file1"),
                            ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "with_missing",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="with_missing"),
                children=[
                    GroupDefault(group="db", value="???"),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "placeholder",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="placeholder"),
                children=[
                    GroupDefault(group="group1"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="placeholder",
        ),
        param(
            "placeholder",
            ["group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="placeholder"),
                children=[
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="placeholder"),
                        children=[
                            GroupDefault(group="group2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="placeholder"),
                        children=[
                            GroupDefault(group="group2", value="file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "interpolation_simple",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_simple"),
                children=[
                    GroupDefault(group="group1", value="file1"),
                    GroupDefault(group="group2", value="file2"),
                    GroupDefault(group="group1_group2", value="file1_file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file2"),
                    GroupDefault(group="group2", value="file2"),
                    GroupDefault(group="group1_group2", value="file2_file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1_group2", value="file1_file2"),
                    GroupDefault(group="group1", value="file1"),
                    GroupDefault(group="group2", value="file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1_group2", value="file2_file2"),
                    GroupDefault(group="group1", value="file2"),
                    GroupDefault(group="group2", value="file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1/group2", value="file1"),
                    GroupDefault(group="group1_group2", value="foo_file1"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1/group2", value="file2"),
                    GroupDefault(group="group1_group2", value="foo_file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1", package="package"),
                    GroupDefault(group="group2", value="file2"),
                    GroupDefault(group="group1_group2", value="file1_file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file2", package="package"),
                    GroupDefault(group="group2", value="file2"),
                    GroupDefault(group="group1_group2", value="file2_file2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1"),
                    GroupDefault(group="group2", value="file1"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1_group2",
                            value="file1_file1_with_defaults_list",
                        ),
                        children=[
                            ConfigDefault(path="empty1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1"),
                    GroupDefault(group="group2", value="file2"),
                    DefaultsTreeNode(
                        node=GroupDefault(
                            group="group1_group2",
                            value="file1_file2_with_defaults_list",
                        ),
                        children=[
                            ConfigDefault(path="empty2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    dedent(
                        """\
                group1_group2/file1_file1_defaults_with_override: Default List Overrides are not allowed in the subtree
                of an in interpolated config group (override group1_group2/foo=bar).
                """
                    )
                ),
            ),
            id="interpolation_with_nested_defaults_list_with_override",
        ),
        param(
            "interpolation_in_nested",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "In 'group1/interpolation': Defaults List interpolation is only supported in the primary config"
                ),
            ),
            id="interpolation_in_nested",
        ),
        param(
            "interpolation_config_default",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_config_default"),
                children=[
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="group1/group2/file1"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="interpolation_config_default",
        ),
        param(
            "interpolation_bad_key",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "Error resolving interpolation '${not_found}', possible interpolation keys: group1"
                ),
            ),
            id="interpolation_bad_key",
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "interpolation_legacy_with_self",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="interpolation_legacy_with_self"),
                children=[
                    ConfigDefault(path="_self_"),
                    GroupDefault(group="group1", value="file1"),
                    GroupDefault(group="group2", value="file2"),
                    GroupDefault(group="group1_group2", value="file1_file2"),
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
                    GroupDefault(group="group1", value="file1"),
                    GroupDefault(group="group2", value="file2"),
                    GroupDefault(group="group1_group2", value="file1_file2"),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "override_nested_to_null",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="override_nested_to_null"),
                children=[
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "include_nested_group",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group"),
                children=[
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file1"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="group_item1", deleted=True),
                    ConfigDefault(path="_self_"),
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
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1"),
                        children=[
                            GroupDefault(group="group2", value="file1", deleted=True),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="group_item1", deleted=True),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1", package="pkg1"),
                    GroupDefault(group="group1", value="file1", package="pkg2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(
                        group="group1", value="file1", package="pkg1", deleted=True
                    ),
                    GroupDefault(group="group1", value="file1", package="pkg2"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file1", package="pkg1"),
                    GroupDefault(
                        group="group1", value="file1", package="pkg2", deleted=True
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "not_found",
            [],
            raises(
                ConfigCompositionException,
                match="^Cannot find primary config 'not_found'. Check that it's in your config search path.",
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


@mark.parametrize(
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
        param(
            "empty",
            ["+group1=override_invalid"],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "In 'group1/override_invalid': Could not override 'group1/group2@group1.foo'."
                    "\nDid you mean to override group1/group2?"
                ),
            ),
            id="nested_override_invalid_group",
        ),
        param(
            "empty",
            ["+group1=override_invalid2"],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "In 'group1/override_invalid2': Could not override 'group1/group2'."
                    "\nDid you mean to override group1/group2@group1.foo?"
                ),
            ),
            id="nested_override_invalid_group",
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "missing_optional_default",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="missing_optional_default"),
                children=[
                    ConfigDefault(path="empty"),
                    GroupDefault(
                        group="foo", value="missing", optional=True, deleted=True
                    ),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "group_default_global",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default_global"),
                children=[
                    GroupDefault(group="group1", value="file_with_global_header"),
                    ConfigDefault(path="_self_"),
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
                    GroupDefault(group="group1", value="file_with_global_header"),
                    ConfigDefault(path="_self_"),
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


@mark.parametrize(
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
                children=[GroupDefault(group="group1", value="file1")],
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


@mark.parametrize(
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
                            GroupDefault(group="help", value="default"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
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
                            GroupDefault(group="help", value="default"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    VirtualRoot(),
                    GroupDefault(group="group1", value="file1"),
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


@mark.parametrize(
    ("config_name", "overrides", "expected"),
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
                            GroupDefault(group="help", value="custom1"),
                            GroupDefault(group="output", value="default"),
                            ConfigDefault(path="_self_"),
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


@mark.parametrize(
    ("config_name", "overrides", "expected"),
    [
        param(
            "keyword_as_groups",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="keyword_as_groups"),
                children=[
                    GroupDefault(group="optional", value="file1"),
                    GroupDefault(group="override", value="file1"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="keyword_override_as_group",
        ),
        param(
            "keyword_override_override",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="keyword_override_override"),
                children=[
                    GroupDefault(group="override", value="file2"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="keyword_override_override",
        ),
        param(
            "keyword_optional_optional",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="keyword_optional_optional"),
                children=[
                    GroupDefault(group="optional", value="file1", optional=True),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="keyword_optional_optional",
        ),
    ],
)
def test_group_with_keyword_names(
    config_name: Optional[str],
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )


@mark.parametrize(
    ("config_name", "overrides", "expected", "expected_choices"),
    [
        param(
            "empty",
            [],
            DefaultsTreeNode(node=ConfigDefault(path="empty")),
            {},
            id="empty",
        ),
        param(
            "group_default",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            {"group1": "file1"},
            id="group_default",
        ),
        param(
            "group_default",
            ["group1=file2"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group_default"),
                children=[
                    GroupDefault(group="group1", value="file2"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            {"group1": "file2"},
            id="group_default:override",
        ),
        param(
            "nested_placeholder",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="nested_placeholder"),
                children=[
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="placeholder"),
                        children=[
                            GroupDefault(group="group2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
                ],
            ),
            {"group1": "placeholder", "group1/group2": None},
            id="nested_placeholder",
        ),
        param(
            "include_nested_group_pkg2",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="include_nested_group_pkg2"),
                children=[
                    DefaultsTreeNode(
                        node=GroupDefault(group="group1", value="group_item1_pkg2"),
                        children=[
                            GroupDefault(group="group2", value="file1", package="pkg2"),
                            ConfigDefault(path="_self_"),
                        ],
                    ),
                    ConfigDefault(path="_self_"),
                ],
            ),
            {"group1": "group_item1_pkg2", "group1/group2@group1.pkg2": "file1"},
            id="include_nested_group_pkg2",
        ),
    ],
)
def test_choices(
    config_name: Optional[str],
    overrides: List[str],
    expected: DefaultsTreeNode,
    expected_choices: Dict[str, str],
) -> None:
    res = _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )
    assert res is not None
    assert res.overrides.known_choices == expected_choices


@mark.parametrize(
    ("config_name", "overrides", "package_header", "expected"),
    [
        param(
            "deprecated_headers/group",
            [],
            "_group_",
            DefaultsTreeNode(node=ConfigDefault(path="deprecated_headers/group")),
            id="deprecated_headers/group",
        ),
        param(
            "deprecated_headers/name",
            [],
            "_name_",
            DefaultsTreeNode(node=ConfigDefault(path="deprecated_headers/name")),
            id="deprecated_headers/name",
        ),
        param(
            "deprecated_headers/group_name",
            [],
            "_group_._name_",
            DefaultsTreeNode(node=ConfigDefault(path="deprecated_headers/group_name")),
            id="deprecated_headers/group_name",
        ),
        param(
            "deprecated_headers/group_foo",
            [],
            "_group_.foo",
            DefaultsTreeNode(node=ConfigDefault(path="deprecated_headers/group_foo")),
            id="deprecated_headers/group_foo",
        ),
    ],
)
def test_deprecated_package_header_keywords(
    config_name: Optional[str],
    overrides: List[str],
    package_header: str,
    expected: DefaultsTreeNode,
) -> None:
    msg = dedent(
        f"""\
        In '{config_name}': Usage of deprecated keyword in package header '# @package {package_header}'.
        See https://hydra.cc/docs/next/upgrades/1.0_to_1.1/changes_to_package_header for more information"""
    )
    with warns(UserWarning, match=re.escape(msg)):
        _test_defaults_tree_impl(
            config_name=config_name,
            input_overrides=overrides,
            expected=expected,
        )


@mark.parametrize(
    ("config_name", "overrides", "expected"),
    [
        param(
            "select_multi",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi"),
                children=[
                    ConfigDefault(path="group1/file1"),
                    ConfigDefault(path="group1/file2"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi",
        ),
        param(
            "select_multi",
            ["group1=[file1,file3]"],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi"),
                children=[
                    ConfigDefault(path="group1/file1"),
                    ConfigDefault(path="group1/file3"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi:override_list",
        ),
        param(
            "select_multi",
            ["group1=[]"],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi"),
                children=[ConfigDefault(path="_self_")],
            ),
            id="select_multi:override_to_empty_list",
        ),
        param(
            "select_multi",
            ["group1=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi"),
                children=[
                    GroupDefault(group="group1", value="file1"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi:override_to_option",
        ),
        # nested
        param(
            "group1/select_multi",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group1/select_multi"),
                children=[
                    ConfigDefault(path="group2/file1"),
                    ConfigDefault(path="group2/file2"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="group1/select_multi",
        ),
        param(
            "group1/select_multi",
            ["group1/group2=[file1,file3]"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group1/select_multi"),
                children=[
                    ConfigDefault(path="group2/file1"),
                    ConfigDefault(path="group2/file3"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="group1/select_multi:override",
        ),
        param(
            "select_multi_interpolation",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "In 'select_multi_interpolation': "
                    "Defaults List interpolation is not supported in options list items"
                ),
            ),
            id="select_multi_interpolation",
        ),
        param(
            "select_multi_override",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi_override"),
                children=[
                    ConfigDefault(path="group1/file3"),
                    ConfigDefault(path="group1/file1"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi_override",
        ),
        param(
            "select_multi_optional",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi_optional"),
                children=[
                    ConfigDefault(path="group1/not_found", deleted=True, optional=True),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi_optional",
        ),
        param(
            "select_multi_optional",
            ["group1=[file1,not_found2]"],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi_optional"),
                children=[
                    ConfigDefault(path="group1/file1", optional=True),
                    ConfigDefault(
                        path="group1/not_found2", deleted=True, optional=True
                    ),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi_optional:override",
        ),
    ],
)
def test_select_multi(
    config_name: Optional[str],
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )


@mark.parametrize(
    ("config_name", "overrides", "expected"),
    [
        param(
            "select_multi_pkg",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi_pkg"),
                children=[
                    ConfigDefault(path="group1/file1", package="foo"),
                    ConfigDefault(path="group1/file2", package="foo"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi",
        ),
        param(
            "select_multi_pkg",
            ["group1@foo=[file1,file3]"],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi_pkg"),
                children=[
                    ConfigDefault(path="group1/file1", package="foo"),
                    ConfigDefault(path="group1/file3", package="foo"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi_pkg:override_list",
        ),
        param(
            "select_multi_pkg",
            ["group1@foo=[]"],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi_pkg"),
                children=[ConfigDefault(path="_self_")],
            ),
            id="select_multi_pkg:override_to_empty_list",
        ),
        param(
            "select_multi_pkg",
            ["group1@foo=file1"],
            DefaultsTreeNode(
                node=ConfigDefault(path="select_multi_pkg"),
                children=[
                    GroupDefault(group="group1", value="file1", package="foo"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="select_multi_pkg:override_to_option",
        ),
        # nested
        param(
            "group1/select_multi_pkg",
            [],
            DefaultsTreeNode(
                node=ConfigDefault(path="group1/select_multi_pkg"),
                children=[
                    ConfigDefault(path="group2/file1", package="bar"),
                    ConfigDefault(path="group2/file2", package="bar"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="group1/select_multi_pkg",
        ),
        param(
            "group1/select_multi_pkg",
            ["group1/group2@group1.bar=[file1,file3]"],
            DefaultsTreeNode(
                node=ConfigDefault(path="group1/select_multi_pkg"),
                children=[
                    ConfigDefault(path="group2/file1", package="bar"),
                    ConfigDefault(path="group2/file3", package="bar"),
                    ConfigDefault(path="_self_"),
                ],
            ),
            id="group1/select_multi:override",
        ),
    ],
)
def test_select_multi_pkg(
    config_name: Optional[str],
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )


@mark.parametrize(
    ("config_name", "overrides", "expected"),
    [
        param(
            "experiment/error_override_without_abs_and_header",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "In 'experiment/error_override_without_abs_and_header': "
                    "Could not override 'experiment/group1'. No match in the defaults list"
                ),
            ),
            id="experiment/error_override_without_abs_and_header",
        ),
        param(
            "experiment/error_override_without_global",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "In 'experiment/error_override_without_global': "
                    "Could not override 'group1@experiment.group1'. No match in the defaults list"
                ),
            ),
            id="experiment/error_override_without_global",
        ),
    ],
)
def test_nested_override_errors(
    config_name: Optional[str],
    overrides: List[str],
    expected: DefaultsTreeNode,
) -> None:
    _test_defaults_tree_impl(
        config_name=config_name,
        input_overrides=overrides,
        expected=expected,
    )
