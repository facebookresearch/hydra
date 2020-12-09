# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from textwrap import dedent
from typing import Any, List

from pytest import mark, param, raises

from hydra._internal.new_defaults_list import create_defaults_list
from hydra.core.new_default_element import (
    ConfigDefault,
    GroupDefault,
    InputDefault,
    ResultDefault,
)
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.errors import ConfigCompositionException
from hydra.test_utils.test_utils import chdir_hydra_root
from tests.defaults_list import create_repo

chdir_hydra_root()

# registers config source plugins
Plugins.instance()


# TODO: (Y) Test with simple config group overrides
# TODO: (Y) Test computed package when there are no package overrides in package header
# TODO: (Y) test with config group overrides overriding config groups @pkg
# TODO: (Y) test overriding config group choices with non-default packages
#   packages to test:
#    (Y) _global_
#    (Y) _global_.foo
#    (Y) _name_
# TODO: (Y) test with config header package override
# TODO: (Y) test with both config header and defaults list pkg override
# TODO: Support overriding config group values from the defaults list
#  - (Y) reconsider support for overriding as before, DECISION: Not happening.
#  - (Y) Support marked overrides in primary config only
#  - (Y) Support marked override in all configs
#  - (Y) Test overriding of config groups with a specified package (@pkg)
#  - (Y) Overriding of config groups with a specified package (@pkg) when there are multiple choices from same group
#  - (Y) Handle hydra overrides
# TODO: Experiment use case: test the following from a config in an experiment group
#  - (Y) Override user config group with and without an external override of the same config group
#  - (Y) Experiment specified in primary defaults
#  - (Y) Append experiment file from external overrides
#  - (Y) Override hydra config group from experiment [+ external override]
#  - (Y) Include config with an absolute path
#  - (Y) Test final defaults list with an experiment file
#  - (Y) Test experiment config as a primary (must have @package _global_ and absolute addressing of config groups)
# TODO: (Y) package header:
#  - (Y) Consider making relative. Decision: package header will remain absolute.
#  - (Y) Consider deprecating completely. Decision: package will not be deprecated for now
# TODO: (Y) Test use cases for config extension:
#  - (Y) Extension from the same config group
#  - (Y) Extension from absolute config group
#  - (Y) Extension from a nested config group
# TODO: (Y) Test missing ('???') in Defaults List
# TODO: (Y) Support placeholder element
# TODO: Interpolation support
#  - (Y) Simple + override
#  - (Y) Forward + override
#  - (Y) Interpolate with nested groups
#  - (Y) Interpolate with group@pkg1
#  - (Y) Test interpolated config with a defaults list
#  - (Y) Error if interpolated config defaults list has an overrides
#  - (Y) Support and deprecate legacy defaults list interpolation style
# TODO: delete support from overrides
#  - (Y) override to null from defaults list
#  - (Y) Support delete by group
#  - (Y) Support delete by group=value
#  - (Y) Test deletion with a specific package
#  - (Y) Deletion test with final defaults list
# TODO: Error handling:
#  - (Y) Error handling for overrides that did not match any config group in the defaults list
#  - (Y) Error if delete override did not delete anything
#  - (Y) Duplicate _self_ error
#  - (Y) test handling missing configs mentioned in defaults list
#  - (Y) Ambiguous overrides should provide valid override keys for group
#  - (Y) Test deprecation message when attempting to override hydra configs without override: true
#  - (Y) duplicate entries in final defaults list raises an error


# TODO: Integrate with Hydra
#  - replace old defaults list computation
#  - enable --info=defaults output
#  - ensure all tests are passing

# TODO: (Y) rename support:
#  - (Y) Remove rename support form 1.1
#  - Deprecate rename support in 1.0


# TODO: cleanup
#  - Remove previous implementation of recursive defaults list and rename new_defaults_list to defaults_list etc.
#  - Clean up package logic from config sources
#  - Clean up Hydra 1.0 warnings related to package header
#  - Delete tests and test data of old defaults list impl


# TODO Documentation
#  - Update defaults list documentation
#  - Create a page describing configuring experiments with Hydra (experiment use case)
#  - Create https://hydra.cc/docs/next/upgrades/1.0_to_1.1/default_list_override


@mark.parametrize(  # type: ignore
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
def test_loaded_defaults_list(
    config_path: str, expected_list: List[InputDefault]
) -> None:
    repo = create_repo()
    result = repo.load_config(config_path=config_path, is_primary_config=True)
    assert result is not None
    assert result.new_defaults_list == expected_list


def _test_defaults_list_impl(
    config_name: str,
    overrides: List[str],
    expected: Any,
    prepend_hydra: bool = False,
    skip_missing: bool = False,
) -> None:
    parser = OverridesParser.create()
    repo = create_repo()
    overrides_list = parser.parse_overrides(overrides=overrides)
    if isinstance(expected, list) or expected is None:
        result = create_defaults_list(
            repo=repo,
            config_name=config_name,
            overrides_list=overrides_list,
            prepend_hydra=prepend_hydra,
            skip_missing=skip_missing,
        )
        assert result.defaults == expected
    else:
        with expected:
            create_defaults_list(
                repo=repo,
                config_name=config_name,
                overrides_list=overrides_list,
                prepend_hydra=prepend_hydra,
                skip_missing=skip_missing,
            )


@mark.parametrize(  # type: ignore
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
        # absolute group
        param(
            ConfigDefault(path="/foo/zoo", parent_base_dir="irrelevant"),
            "foo",
            "foo/zoo",
            id="config_default:absolute",
        ),
        param(
            GroupDefault(group="/foo", name="zoo", parent_base_dir="irrelevant"),
            "foo",
            "foo/zoo",
            id="group_default:absolute",
        ),
    ],
)
def test_get_paths(
    default: InputDefault, expected_group_path: Any, expected_config_path: Any
) -> None:
    assert default.get_group_path() == expected_group_path
    assert default.get_config_path() == expected_config_path


@mark.parametrize(  # type: ignore
    "default,expected",
    [
        param(
            ConfigDefault(path="bar", parent_base_dir=""),
            "",
            id="config_default",
        ),
        param(
            ConfigDefault(path="foo/bar", parent_base_dir=""),
            "foo",
            id="config_default",
        ),
        param(
            ConfigDefault(path="bar", parent_base_dir="foo"),
            "foo",
            id="config_default",
        ),
        param(
            ConfigDefault(path="bar", parent_base_dir="a/b"),
            "a.b",
            id="config_default",
        ),
        param(
            GroupDefault(group="a", name="a1", parent_base_dir=""),
            "a",
            id="group_default",
        ),
        param(
            GroupDefault(group="a/b", name="a1", parent_base_dir=""),
            "a.b",
            id="group_default",
        ),
        param(
            GroupDefault(group="a/b", name="a1", parent_base_dir="x"),
            "x.a.b",
            id="group_default",
        ),
        # absolute group/path
        param(
            ConfigDefault(path="/foo/bar", parent_base_dir="irrelevant"),
            "foo",
            id="config_default:absolute",
        ),
        param(
            GroupDefault(group="/foo", name="bar", parent_base_dir="irrelevant"),
            "foo",
            id="group_default:absolute",
        ),
    ],
)
def test_get_default_package(default: InputDefault, expected: Any) -> None:
    assert default.get_default_package() == expected


@mark.parametrize(  # type: ignore
    "default,parent_package, parent_base_dir, expected",
    [
        # empty parent package
        param(
            ConfigDefault(path="bar"),
            "",
            "",
            "",
            id="config_default:path=bar,parent_package=,package=",
        ),
        param(
            ConfigDefault(path="group1/bar"),
            "",
            "",
            "group1",
            id="config_default:path=group1/bar,parent_package=, package=",
        ),
        param(
            ConfigDefault(path="bar", package="pkg1"),
            "",
            "",
            "pkg1",
            id="config_default:path=bar,parent_package=, package=pkg1",
        ),
        param(
            ConfigDefault(path="group1/bar", package="pkg1"),
            "",
            "",
            "pkg1",
            id="config_default:path=group1/bar,parent_package=,package=pkg1",
        ),
        # non empty parent package
        param(
            ConfigDefault(path="bar", package="pkg1"),
            "a",
            "",
            "a.pkg1",
            id="config_default:path=bar,parent_package=a, package=pkg1",
        ),
        # global package
        param(
            ConfigDefault(
                path="bar",
                package="_global_.pkg1",
            ),
            "",
            "",
            "pkg1",
            id="config_default:parent_package=a, package=_global_.pkg1",
        ),
        # global parent package
        param(
            ConfigDefault(path="bar", package="pkg1"),
            "_global_.foo",
            "",
            "foo.pkg1",
            id="config_default:parent_package=_global_.foo, package=pkg1",
        ),
        # both globals
        param(
            ConfigDefault(path="bar", package="_global_.pkg1"),
            "_global_.foo",
            "",
            "pkg1",
            id="config_default:parent_package=_global_.foo, package=_global_.pkg1",
        ),
        # _group_
        param(
            GroupDefault(group="foo", name="bar", package="_group_"),
            "",
            "",
            "foo",
            id="group_default:parent_package=, package=_group_",
        ),
        param(
            ConfigDefault(path="foo/bar", package="_group_"),
            "",
            "",
            "foo",
            id="config_default:parent_package=, package=_group_",
        ),
        param(
            GroupDefault(group="foo", name="bar", package="_group_.zoo"),
            "",
            "",
            "foo.zoo",
            id="group_default:parent_package=, package=_group_.zoo",
        ),
        param(
            ConfigDefault(
                path="foo/bar",
                package="_group_.zoo",
            ),
            "",
            "",
            "foo.zoo",
            id="config_default:parent_package=, package=_group_.zoo",
        ),
    ],
)
def test_get_final_package(
    default: InputDefault, parent_package: str, parent_base_dir: str, expected: Any
) -> None:
    default.update_parent(
        parent_base_dir=parent_base_dir, parent_package=parent_package
    )
    assert default.get_final_package() == expected


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "empty",
            [],
            [ResultDefault(config_path="empty", package="")],
            id="empty",
        ),
        param(
            "config_default",
            [],
            [
                ResultDefault(config_path="config_default", package="", is_self=True),
                ResultDefault(config_path="empty", package="", parent="config_default"),
            ],
            id="config_default",
        ),
        param(
            "group_default",
            [],
            [
                ResultDefault(config_path="group_default", package="", is_self=True),
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="group_default"
                ),
            ],
            id="group_default",
        ),
        param(
            "self_leading",
            [],
            [
                ResultDefault(config_path="self_leading", package="", is_self=True),
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="self_leading"
                ),
            ],
            id="self_leading",
        ),
        param(
            "self_trailing",
            [],
            [
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="self_trailing"
                ),
                ResultDefault(config_path="self_trailing", package="", is_self=True),
            ],
            id="self_trailing",
        ),
        param(
            "include_nested_group",
            [],
            [
                ResultDefault(
                    config_path="include_nested_group", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/group_item1",
                    parent="include_nested_group",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.group2",
                    parent="group1/group_item1",
                ),
            ],
            id="include_nested_group",
        ),
    ],
)
def test_simple_defaults_list_cases(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "config_default_pkg1",
            [],
            [
                ResultDefault(
                    config_path="config_default_pkg1", package="", is_self=True
                ),
                ResultDefault(
                    config_path="empty", package="pkg1", parent="config_default_pkg1"
                ),
            ],
            id="config_default_pkg1",
        ),
        param(
            "include_nested_config_item_pkg2",
            [],
            [
                ResultDefault(
                    config_path="include_nested_config_item_pkg2",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/config_item_pkg2",
                    parent="include_nested_config_item_pkg2",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.pkg2",
                    parent="group1/config_item_pkg2",
                ),
            ],
            id="include_nested_config_item_pkg2",
        ),
        param(
            "include_nested_config_item_global",
            [],
            [
                ResultDefault(
                    config_path="include_nested_config_item_global",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/config_item_global_",
                    parent="include_nested_config_item_global",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="",
                    parent="group1/config_item_global_",
                ),
            ],
            id="include_nested_config_item_global",
        ),
    ],
)
def test_override_package_in_defaults_list(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_pkg2",
            [],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg2", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg2",
                    parent="include_nested_group_pkg2",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.pkg2",
                    parent="group1/group_item1_pkg2",
                ),
            ],
            id="include_nested_group_pkg2",
        ),
        param(
            "include_nested_group_pkg2",
            ["group1/group2@group1.pkg2=file2"],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg2", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg2",
                    parent="include_nested_group_pkg2",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="group1.pkg2",
                    parent="group1/group_item1_pkg2",
                ),
            ],
            id="option_override:include_nested_group_pkg2",
        ),
    ],
)
def test_include_nested_group_pkg2(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "group_default_pkg1",
            [],
            [
                ResultDefault(
                    config_path="group_default_pkg1", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/file1",
                    package="pkg1",
                    parent="group_default_pkg1",
                ),
            ],
            id="group_default_pkg1",
        ),
        param(
            "group_default_pkg1",
            ["group1@pkg1=file2"],
            [
                ResultDefault(
                    config_path="group_default_pkg1", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/file2",
                    package="pkg1",
                    parent="group_default_pkg1",
                ),
            ],
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
    ],
)
def test_group_default_pkg1(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_global_",
            [],
            [
                ResultDefault(
                    config_path="include_nested_group_global_",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_",
                    parent="include_nested_group_global_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="",
                    parent="group1/group_item1_global_",
                ),
            ],
            id="include_nested_config_item_global",
        ),
        param(
            "include_nested_group_global_",
            ["group1/group2@=file2"],
            [
                ResultDefault(
                    config_path="include_nested_group_global_",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_",
                    parent="include_nested_group_global_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="",
                    parent="group1/group_item1_global_",
                ),
            ],
            id="option_override:include_nested_config_item_global",
        ),
    ],
)
def test_include_nested_group_global(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_global_foo",
            [],
            [
                ResultDefault(
                    config_path="include_nested_group_global_foo",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_foo",
                    parent="include_nested_group_global_foo",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="foo",
                    parent="group1/group_item1_global_foo",
                ),
            ],
            id="include_nested_group_global_foo",
        ),
        param(
            "include_nested_group_global_foo",
            ["group1/group2@foo=file2"],
            [
                ResultDefault(
                    config_path="include_nested_group_global_foo",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_foo",
                    parent="include_nested_group_global_foo",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="foo",
                    parent="group1/group_item1_global_foo",
                ),
            ],
            id="include_nested_group_global_foo",
        ),
    ],
)
def test_include_nested_group_global_foo(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_name_",
            [],
            [
                ResultDefault(
                    config_path="include_nested_group_name_",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_name_",
                    parent="include_nested_group_name_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.file1",
                    parent="group1/group_item1_name_",
                ),
            ],
            id="include_nested_group_name_",
        ),
        param(
            "include_nested_group_name_",
            ["group1/group2@group1.file1=file2"],
            [
                ResultDefault(
                    config_path="include_nested_group_name_",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_name_",
                    parent="include_nested_group_name_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="group1.file2",
                    parent="group1/group_item1_name_",
                ),
            ],
            id="include_nested_group_name_",
        ),
    ],
)
def test_include_nested_group_name_(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "primary_pkg_header_foo",
            [],
            [
                ResultDefault(
                    config_path="primary_pkg_header_foo",
                    package="foo",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/file1",
                    package="foo.group1",
                    parent="primary_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/file1",
                    package="foo.pkg",
                    parent="primary_pkg_header_foo",
                ),
            ],
            id="primary_pkg_header_foo",
        ),
        param(
            "primary_pkg_header_foo",
            ["group1@foo.group1=file2", "group1@foo.pkg=file3"],
            [
                ResultDefault(
                    config_path="primary_pkg_header_foo",
                    package="foo",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/file2",
                    package="foo.group1",
                    parent="primary_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/file3",
                    package="foo.pkg",
                    parent="primary_pkg_header_foo",
                ),
            ],
            id="primary_pkg_header_foo",
        ),
    ],
)
def test_primary_cfg_pkg_header_foo(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_pkg_header_foo",
            [],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    package="foo",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="foo.group2",
                    parent="group1/group_item1_pkg_header_foo",
                ),
            ],
            id="include_nested_group_pkg_header_foo",
        ),
        param(
            "include_nested_group_pkg_header_foo",
            ["group1/group2@foo.group2=file2"],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    package="foo",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="foo.group2",
                    parent="group1/group_item1_pkg_header_foo",
                ),
            ],
            id="include_nested_group_pkg_header_foo:override_nested",
        ),
        param(
            "include_nested_group_pkg_header_foo",
            ["group1=group_item2_pkg_header_foo"],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item2_pkg_header_foo",
                    package="foo",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="foo.group2",
                    parent="group1/group_item2_pkg_header_foo",
                ),
            ],
            id="include_nested_group_pkg_header_foo:override_first_level",
        ),
        param(
            "include_nested_group_pkg_header_foo",
            ["group1=group_item2_pkg_header_bar"],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item2_pkg_header_bar",
                    package="bar",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="bar.group2",
                    parent="group1/group_item2_pkg_header_bar",
                ),
            ],
            id="include_nested_group_pkg_header_foo:override_first_level_with_package_header_change",
        ),
    ],
)
def test_include_nested_group_pkg_header_foo(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "empty",
            ["+group1/group2=file1_pkg_header_foo"],
            [
                ResultDefault(config_path="empty", package="", is_self=True),
                ResultDefault(
                    config_path="group1/group2/file1_pkg_header_foo",
                    parent="empty",
                    package="foo",
                ),
            ],
            id="included_from_overrides",
        ),
        param(
            "empty",
            ["+group1=group_item1_with_pkg_header_foo"],
            [
                ResultDefault(config_path="empty", package="", is_self=True),
                ResultDefault(
                    config_path="group1/group_item1_with_pkg_header_foo",
                    parent="empty",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1_pkg_header_foo",
                    parent="group1/group_item1_with_pkg_header_foo",
                    package="foo",
                    is_self=False,
                ),
            ],
            id="included_from_overrides",
        ),
    ],
)
def test_nested_package_header_is_absolute(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_pkg_header_foo_override_pkg_bar",
            [],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo_override_pkg_bar",
                    parent=None,
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    parent="include_nested_group_pkg_header_foo_override_pkg_bar",
                    package="bar",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    parent="group1/group_item1_pkg_header_foo",
                    package="bar.group2",
                    is_self=False,
                ),
            ],
            id="include_nested_group_global_foo_override_pkg_bar",
        ),
        param(
            "include_nested_group_pkg_header_foo_override_pkg_bar",
            ["group1@bar=group_item2"],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo_override_pkg_bar",
                    parent=None,
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item2",
                    parent="include_nested_group_pkg_header_foo_override_pkg_bar",
                    package="bar",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    parent="group1/group_item2",
                    package="bar.group2",
                    is_self=False,
                ),
            ],
            id="include_nested_group_global_foo_override_pkg_bar:override_group1",
        ),
        param(
            "include_nested_group_pkg_header_foo_override_pkg_bar",
            ["group1/group2@bar.group2=file2"],
            [
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo_override_pkg_bar",
                    parent=None,
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    parent="include_nested_group_pkg_header_foo_override_pkg_bar",
                    package="bar",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file2",
                    parent="group1/group_item1_pkg_header_foo",
                    package="bar.group2",
                    is_self=False,
                ),
            ],
            id="include_nested_group_global_foo_override_pkg_bar:override_group2",
        ),
    ],
)
def test_overriding_package_header_from_defaults_list(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "empty",
            [],
            [
                ResultDefault(
                    config_path="hydra/config",
                    parent="<root>",
                    package="hydra",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="hydra/help/default",
                    parent="hydra/config",
                    package="hydra.help",
                ),
                ResultDefault(
                    config_path="hydra/output/default",
                    parent="hydra/config",
                    package="hydra",
                ),
                ResultDefault(config_path="empty", parent="<root>", package=""),
            ],
            id="just_hydra_config",
        ),
        param(
            "legacy_override_hydra",
            [],
            [
                ResultDefault(
                    config_path="hydra/config",
                    parent="<root>",
                    package="hydra",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="hydra/help/custom1",
                    parent="hydra/config",
                    package="hydra.help",
                    is_self=False,
                ),
                ResultDefault(
                    config_path="hydra/output/default",
                    parent="hydra/config",
                    package="hydra",
                    is_self=False,
                ),
                ResultDefault(
                    config_path="legacy_override_hydra",
                    parent="<root>",
                    package="",
                    is_self=True,
                ),
            ],
            id="override_hydra",
        ),
    ],
)
def test_with_hydra_config(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
    recwarn: Any,  # Testing deprecated behavior
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
        prepend_hydra=True,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=include_absolute_config"],
            [
                ResultDefault(config_path="group_default", package="", is_self=True),
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="group_default"
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.group2",
                    parent="experiment/include_absolute_config",
                ),
                ResultDefault(
                    config_path="experiment/include_absolute_config",
                    package="",
                    parent="group_default",
                    is_self=True,
                ),
            ],
            id="group_default:experiment=include_absolute_config",
        ),
    ],
)
def test_experiment_use_case(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "experiment/override_hydra",
            [],
            [
                ResultDefault(
                    config_path="hydra/config",
                    package="hydra",
                    parent="<root>",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="hydra/help/custom1",
                    package="hydra.help",
                    parent="hydra/config",
                ),
                ResultDefault(
                    config_path="hydra/output/default",
                    package="hydra",
                    parent="hydra/config",
                ),
                ResultDefault(
                    config_path="experiment/override_hydra",
                    package="",
                    parent="<root>",
                    is_self=True,
                ),
            ],
            id="group_default:experiment=include_absolute_config",
        ),
    ],
)
def test_as_as_primary(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
        prepend_hydra=True,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "placeholder",
            [],
            [ResultDefault(config_path="placeholder", package="", is_self=True)],
            id="placeholder",
        ),
        param(
            "placeholder",
            ["group1=file1"],
            [
                ResultDefault(config_path="placeholder", package="", is_self=True),
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="placeholder"
                ),
            ],
            id="placeholder:override",
        ),
        param(
            "nested_placeholder",
            [],
            [
                ResultDefault(
                    config_path="nested_placeholder", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/placeholder",
                    package="group1",
                    parent="nested_placeholder",
                    is_self=True,
                ),
            ],
            id="nested_placeholder",
        ),
        param(
            "nested_placeholder",
            ["group1/group2=file1"],
            [
                ResultDefault(
                    config_path="nested_placeholder", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/placeholder",
                    package="group1",
                    parent="nested_placeholder",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.group2",
                    parent="group1/placeholder",
                ),
            ],
            id="nested_placeholder:override",
        ),
    ],
)
def test_placeholder(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "interpolation_simple",
            ["group1=file2"],
            [
                ResultDefault(
                    config_path="interpolation_simple", package="", is_self=True
                ),
                ResultDefault(
                    config_path="group1/file2",
                    package="group1",
                    parent="interpolation_simple",
                ),
                ResultDefault(
                    config_path="group2/file2",
                    package="group2",
                    parent="interpolation_simple",
                ),
                ResultDefault(
                    config_path="group1_group2/file2_file2",
                    package="group1_group2",
                    parent="interpolation_simple",
                ),
            ],
            id="interpolation_simple",
        ),
        param(
            "interpolation_with_nested_defaults_list",
            [],
            [
                ResultDefault(
                    config_path="interpolation_with_nested_defaults_list",
                    package="",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/file1",
                    package="group1",
                    parent="interpolation_with_nested_defaults_list",
                ),
                ResultDefault(
                    config_path="group2/file1",
                    package="group2",
                    parent="interpolation_with_nested_defaults_list",
                ),
                ResultDefault(
                    config_path="group1_group2/file1_file1_with_defaults_list",
                    package="group1_group2",
                    parent="interpolation_with_nested_defaults_list",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1_group2/empty1",
                    package="group1_group2",
                    parent="group1_group2/file1_file1_with_defaults_list",
                ),
            ],
            id="interpolation_with_nested_defaults_list",
        ),
    ],
)
def test_interpolation_simple(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "include_nested_group",
            ["~group1"],
            [
                ResultDefault(
                    config_path="include_nested_group", package="", is_self=True
                ),
            ],
            id="delete:include_nested_group:group1",
        ),
    ],
)
def test_deletion(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "error_duplicate_group",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "group1 appears more than once in the final defaults list"
                ),
            ),
            id="error_duplicate_group",
        ),
        param(
            "error_duplicate_group_nested",
            [],
            raises(
                ConfigCompositionException,
                match=re.escape(
                    "group1/group2 appears more than once in the final defaults list"
                ),
            ),
            id="error_duplicate_group_nested",
        ),
    ],
)
def test_duplicate_items(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )


@mark.parametrize(  # type: ignore
    "config_name,overrides,expected",
    [
        param(
            "group1/file_with_group_header",
            [],
            [
                ResultDefault(
                    config_path="group1/file_with_group_header", package="group1"
                )
            ],
            id="group1/file_with_group_header",
        ),
        param(
            "empty",
            ["+group1=file_with_group_header"],
            [
                ResultDefault(config_path="empty", package="", is_self=True),
                ResultDefault(
                    config_path="group1/file_with_group_header",
                    package="group1",
                    parent="empty",
                ),
            ],
            id="empty_group1/file_with_group_header",
        ),
        param(
            "group1/group2/file_with_group_header",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file_with_group_header",
                    package="group1.group2",
                )
            ],
            id="group1/group2/file_with_group_header",
        ),
        param(
            "empty",
            ["+group1/group2=file_with_group_header"],
            [
                ResultDefault(config_path="empty", package="", is_self=True),
                ResultDefault(
                    config_path="group1/group2/file_with_group_header",
                    package="group1.group2",
                    parent="empty",
                ),
            ],
            id="empty+group1/group2/file_with_group_header",
        ),
    ],
)
def test_load_group_header(
    config_name: str, overrides: List[str], expected: List[ResultDefault]
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )
