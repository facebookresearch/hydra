# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from textwrap import dedent
from typing import Any, List, Optional

from pytest import mark, param, raises, warns

from hydra._internal.defaults_list import create_defaults_list
from hydra.core.default_element import (
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
            [GroupDefault(group="group1", name="file1", optional=True)],
            id="optional",
        ),
        param(
            "config_default",
            [ConfigDefault(path="empty")],
            id="non_config_group_default",
        ),
    ],
)
def test_loaded_defaults_list(
    config_path: str, expected_list: List[InputDefault]
) -> None:
    repo = create_repo()
    result = repo.load_config(config_path=config_path)
    assert result is not None
    assert result.defaults_list == expected_list


@mark.parametrize(
    "config_path,expected_list",
    [
        param(
            "optional_deprecated",
            [GroupDefault(group="group1", name="file1", optional=True)],
            id="optional",
        ),
    ],
)
def test_deprecated_optional(
    config_path: str, expected_list: List[InputDefault]
) -> None:
    repo = create_repo()
    warning = dedent(
        """
            In optional_deprecated: 'optional: true' is deprecated.
            Use 'optional group1: file1' instead.
            Support for the old style will be removed in Hydra 1.2"""
    )
    with warns(
        UserWarning,
        match=re.escape(warning),
    ):
        result = repo.load_config(config_path=config_path)
    assert result is not None
    assert result.defaults_list == expected_list


def _test_defaults_list_impl(
    config_name: Optional[str],
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


@mark.parametrize(
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


@mark.parametrize(
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


@mark.parametrize(
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
                ResultDefault(config_path="empty", package="", parent="config_default"),
                ResultDefault(config_path="config_default", package="", is_self=True),
            ],
            id="config_default",
        ),
        param(
            "group_default",
            [],
            [
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="group_default"
                ),
                ResultDefault(config_path="group_default", package="", is_self=True),
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
                    config_path="group1/group2/file1",
                    package="group1.group2",
                    parent="group1/group_item1",
                ),
                ResultDefault(
                    config_path="group1/group_item1",
                    parent="include_nested_group",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group", package="", is_self=True
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "config_default_pkg1",
            [],
            [
                ResultDefault(
                    config_path="empty", package="pkg1", parent="config_default_pkg1"
                ),
                ResultDefault(
                    config_path="config_default_pkg1", package="", is_self=True
                ),
            ],
            id="config_default_pkg1",
        ),
        param(
            "include_nested_config_item_pkg2",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.pkg2",
                    parent="group1/config_item_pkg2",
                ),
                ResultDefault(
                    config_path="group1/config_item_pkg2",
                    parent="include_nested_config_item_pkg2",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_config_item_pkg2",
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_config_item_pkg2",
        ),
        param(
            "include_nested_config_item_global",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="",
                    parent="group1/config_item_global_",
                ),
                ResultDefault(
                    config_path="group1/config_item_global_",
                    parent="include_nested_config_item_global",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_config_item_global",
                    package="",
                    is_self=True,
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_pkg2",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.pkg2",
                    parent="group1/group_item1_pkg2",
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg2",
                    parent="include_nested_group_pkg2",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg2", package="", is_self=True
                ),
            ],
            id="include_nested_group_pkg2",
        ),
        param(
            "include_nested_group_pkg2",
            ["group1/group2@group1.pkg2=file2"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="group1.pkg2",
                    parent="group1/group_item1_pkg2",
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg2",
                    parent="include_nested_group_pkg2",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg2", package="", is_self=True
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "group_default_pkg1",
            [],
            [
                ResultDefault(
                    config_path="group1/file1",
                    package="pkg1",
                    parent="group_default_pkg1",
                ),
                ResultDefault(
                    config_path="group_default_pkg1", package="", is_self=True
                ),
            ],
            id="group_default_pkg1",
        ),
        param(
            "group_default_pkg1",
            ["group1@pkg1=file2"],
            [
                ResultDefault(
                    config_path="group1/file2",
                    package="pkg1",
                    parent="group_default_pkg1",
                ),
                ResultDefault(
                    config_path="group_default_pkg1", package="", is_self=True
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_global_",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="",
                    parent="group1/group_item1_global_",
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_",
                    parent="include_nested_group_global_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_global_",
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_config_item_global",
        ),
        param(
            "include_nested_group_global_",
            ["group1/group2@=file2"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="",
                    parent="group1/group_item1_global_",
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_",
                    parent="include_nested_group_global_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_global_",
                    package="",
                    is_self=True,
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_global_foo",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="foo",
                    parent="group1/group_item1_global_foo",
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_foo",
                    parent="include_nested_group_global_foo",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_global_foo",
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_group_global_foo",
        ),
        param(
            "include_nested_group_global_foo",
            ["group1/group2@foo=file2"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="foo",
                    parent="group1/group_item1_global_foo",
                ),
                ResultDefault(
                    config_path="group1/group_item1_global_foo",
                    parent="include_nested_group_global_foo",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_global_foo",
                    package="",
                    is_self=True,
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_name_",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.file1",
                    parent="group1/group_item1_name_",
                ),
                ResultDefault(
                    config_path="group1/group_item1_name_",
                    parent="include_nested_group_name_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_name_",
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_group_name_",
        ),
        param(
            "include_nested_group_name_",
            ["group1/group2@group1.file1=file2"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="group1.file2",
                    parent="group1/group_item1_name_",
                ),
                ResultDefault(
                    config_path="group1/group_item1_name_",
                    parent="include_nested_group_name_",
                    package="group1",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_name_",
                    package="",
                    is_self=True,
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "primary_pkg_header_foo",
            [],
            [
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
                ResultDefault(
                    config_path="primary_pkg_header_foo",
                    package="foo",
                    is_self=True,
                ),
            ],
            id="primary_pkg_header_foo",
        ),
        param(
            "primary_pkg_header_foo",
            ["group1@foo.group1=file2", "group1@foo.pkg=file3"],
            [
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
                ResultDefault(
                    config_path="primary_pkg_header_foo",
                    package="foo",
                    is_self=True,
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_pkg_header_foo",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="foo.group2",
                    parent="group1/group_item1_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    package="foo",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_group_pkg_header_foo",
        ),
        param(
            "include_nested_group_pkg_header_foo",
            ["group1/group2@foo.group2=file2"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="foo.group2",
                    parent="group1/group_item1_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    package="foo",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_group_pkg_header_foo:override_nested",
        ),
        param(
            "include_nested_group_pkg_header_foo",
            ["group1=group_item2_pkg_header_foo"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="foo.group2",
                    parent="group1/group_item2_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="group1/group_item2_pkg_header_foo",
                    package="foo",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_group_pkg_header_foo:override_first_level",
        ),
        param(
            "include_nested_group_pkg_header_foo",
            ["group1=group_item2_pkg_header_bar"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    package="bar.group2",
                    parent="group1/group_item2_pkg_header_bar",
                ),
                ResultDefault(
                    config_path="group1/group_item2_pkg_header_bar",
                    package="bar",
                    is_self=True,
                    parent="include_nested_group_pkg_header_foo",
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo",
                    package="",
                    is_self=True,
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


@mark.parametrize(
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
                ResultDefault(
                    config_path="empty", package="", is_self=True, primary=True
                ),
                ResultDefault(
                    config_path="group1/group2/file1_pkg_header_foo",
                    parent="group1/group_item1_with_pkg_header_foo",
                    package="foo",
                    is_self=False,
                ),
                ResultDefault(
                    config_path="group1/group_item1_with_pkg_header_foo",
                    parent="empty",
                    package="group1",
                    is_self=True,
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


@mark.parametrize(
    "config_name, overrides, expected",
    [
        param(
            "include_nested_group_pkg_header_foo_override_pkg_bar",
            [],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    parent="group1/group_item1_pkg_header_foo",
                    package="bar.group2",
                    is_self=False,
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    parent="include_nested_group_pkg_header_foo_override_pkg_bar",
                    package="bar",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo_override_pkg_bar",
                    parent=None,
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_group_global_foo_override_pkg_bar",
        ),
        param(
            "include_nested_group_pkg_header_foo_override_pkg_bar",
            ["group1@bar=group_item2"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    parent="group1/group_item2",
                    package="bar.group2",
                    is_self=False,
                ),
                ResultDefault(
                    config_path="group1/group_item2",
                    parent="include_nested_group_pkg_header_foo_override_pkg_bar",
                    package="bar",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo_override_pkg_bar",
                    parent=None,
                    package="",
                    is_self=True,
                ),
            ],
            id="include_nested_group_global_foo_override_pkg_bar:override_group1",
        ),
        param(
            "include_nested_group_pkg_header_foo_override_pkg_bar",
            ["group1/group2@bar.group2=file2"],
            [
                ResultDefault(
                    config_path="group1/group2/file2",
                    parent="group1/group_item1_pkg_header_foo",
                    package="bar.group2",
                    is_self=False,
                ),
                ResultDefault(
                    config_path="group1/group_item1_pkg_header_foo",
                    parent="include_nested_group_pkg_header_foo_override_pkg_bar",
                    package="bar",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="include_nested_group_pkg_header_foo_override_pkg_bar",
                    parent=None,
                    package="",
                    is_self=True,
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "empty",
            [],
            [
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
                ResultDefault(
                    config_path="hydra/config",
                    parent="<root>",
                    package="hydra",
                    is_self=True,
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
                    config_path="hydra/config",
                    parent="<root>",
                    package="hydra",
                    is_self=True,
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "group_default",
            ["+experiment=include_absolute_config"],
            [
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="group_default"
                ),
                ResultDefault(config_path="group_default", package="", is_self=True),
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "experiment/override_hydra",
            [],
            [
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
                    config_path="hydra/config",
                    package="hydra",
                    parent="<root>",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="experiment/override_hydra",
                    package="",
                    parent="<root>",
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


@mark.parametrize(
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
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="placeholder"
                ),
                ResultDefault(config_path="placeholder", package="", is_self=True),
            ],
            id="placeholder:override",
        ),
        param(
            "nested_placeholder",
            [],
            [
                ResultDefault(
                    config_path="group1/placeholder",
                    package="group1",
                    parent="nested_placeholder",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="nested_placeholder", package="", is_self=True
                ),
            ],
            id="nested_placeholder",
        ),
        param(
            "nested_placeholder",
            ["group1/group2=file1"],
            [
                ResultDefault(
                    config_path="group1/group2/file1",
                    package="group1.group2",
                    parent="group1/placeholder",
                ),
                ResultDefault(
                    config_path="group1/placeholder",
                    package="group1",
                    parent="nested_placeholder",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="nested_placeholder", package="", is_self=True
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "interpolation_simple",
            ["group1=file2"],
            [
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
                ResultDefault(
                    config_path="interpolation_simple", package="", is_self=True
                ),
            ],
            id="interpolation_simple",
        ),
        param(
            "interpolation_with_nested_defaults_list",
            [],
            [
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
                    config_path="group1_group2/empty1",
                    package="group1_group2",
                    parent="group1_group2/file1_file1_with_defaults_list",
                ),
                ResultDefault(
                    config_path="group1_group2/file1_file1_with_defaults_list",
                    package="group1_group2",
                    parent="interpolation_with_nested_defaults_list",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="interpolation_with_nested_defaults_list",
                    package="",
                    is_self=True,
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


@mark.parametrize(
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


@mark.parametrize(
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


@mark.parametrize(
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


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            None,
            [],
            [],
            id="none",
        ),
        param(
            None,
            ["+group1=file1"],
            [
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="<root>"
                )
            ],
            id="none+group1=file1",
        ),
    ],
)
def test_with_none_primary(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            None,
            [],
            [
                ResultDefault(
                    config_path="hydra/help/default",
                    package="hydra.help",
                    parent="hydra/config",
                ),
                ResultDefault(
                    config_path="hydra/output/default",
                    package="hydra",
                    parent="hydra/config",
                ),
                ResultDefault(
                    config_path="hydra/config",
                    package="hydra",
                    parent="<root>",
                    is_self=True,
                ),
            ],
            id="none",
        ),
        param(
            None,
            ["+group1=file1"],
            [
                ResultDefault(
                    config_path="hydra/help/default",
                    package="hydra.help",
                    parent="hydra/config",
                ),
                ResultDefault(
                    config_path="hydra/output/default",
                    package="hydra",
                    parent="hydra/config",
                ),
                ResultDefault(
                    config_path="hydra/config",
                    package="hydra",
                    parent="<root>",
                    is_self=True,
                ),
                ResultDefault(
                    config_path="group1/file1", package="group1", parent="<root>"
                ),
            ],
            id="none+group1=file1",
        ),
    ],
)
def test_with_none_primary_with_hydra(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
        prepend_hydra=True,
    )


@mark.parametrize(
    "config_name,overrides,expected",
    [
        param(
            "two_config_items",
            [],
            [
                ResultDefault(
                    config_path="group1/file1",
                    package="group1",
                    parent="two_config_items",
                ),
                ResultDefault(
                    config_path="group1/file2",
                    package="group1",
                    parent="two_config_items",
                ),
                ResultDefault(config_path="two_config_items", package="", is_self=True),
            ],
            id="two_config_items",
        ),
    ],
)
def test_two_config_items(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
    )


@mark.parametrize(
    "config_name,overrides,skip_missing,expected",
    [
        param(
            "with_missing",
            [],
            True,
            [
                ResultDefault(config_path="with_missing", package="", is_self=True),
            ],
            id="with_missing:ignore_missing",
        ),
        param(
            "with_missing",
            ["db=base_db"],
            True,
            [
                ResultDefault(
                    config_path="db/base_db", package="db", parent="with_missing"
                ),
                ResultDefault(config_path="with_missing", package="", is_self=True),
            ],
            id="with_missing:ignore_missing+override",
        ),
        param(
            "with_missing",
            [],
            False,
            raises(
                ConfigCompositionException,
                match=re.escape(
                    dedent(
                        """\
                        You must specify 'db', e.g, db=<OPTION>
                        Available options:
                        \tbase_db"""
                    )
                ),
            ),
            id="with_missing:not_ignore_missing",
        ),
    ],
)
def test_with_missing_config(
    config_name: str,
    overrides: List[str],
    skip_missing: bool,
    expected: List[ResultDefault],
) -> None:
    _test_defaults_list_impl(
        config_name=config_name,
        overrides=overrides,
        expected=expected,
        skip_missing=skip_missing,
    )


@mark.parametrize(
    "default,package_header,expected",
    [
        param(
            GroupDefault(group="group1", name="file"),
            "_group_",
            "group1",
            id="gd:_group_",
        ),
        param(
            GroupDefault(group="group1", name="file"),
            "group1",
            "group1",
            id="gd:group1",
        ),
        param(
            GroupDefault(group="group1", name="file"),
            "abc",
            "abc",
            id="gd:abc",
        ),
        param(
            GroupDefault(group="group1", name="file"),
            "_global_",
            "",
            id="gd:_global_",
        ),
        param(
            GroupDefault(group="group1", name="file"),
            "_group_._name_",
            "group1.file",
            id="gd:_group_._name_",
        ),
    ],
)
def test_set_package_header_no_parent_pkg(
    default: InputDefault, package_header: str, expected: str
) -> None:
    default.update_parent(parent_base_dir="", parent_package="")
    default.set_package_header(package_header)
    assert default.get_final_package() == expected


@mark.parametrize(
    "default,package_header,expected",
    [
        param(
            GroupDefault(group="group1", name="file"),
            "_group_",
            "parent_pkg.group1",
            id="gd:_group_",
        ),
    ],
)
def test_set_package_header_with_parent_pkg(
    default: InputDefault, package_header: str, expected: str
) -> None:
    default.update_parent(parent_base_dir="", parent_package="parent_pkg")
    default.set_package_header(package_header)
    assert default.get_final_package() == expected
