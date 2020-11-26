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


# TODO: (Y) Test with simple config group overrides
# TODO: (Y) Test computed package when there are no package overrides in package header
# TODO: test with config group overrides overriding config groups @pkg
# TODO: test with config header package override
# TODO: test with both config header and defaults list pkg override
# TODO: handle hydra overrides
# TODO: test handling missing configs mentioned in defaults list (with and without optional)
# TODO: test overriding configs in absolute location
# TODO: test duplicate _self_ error
# TODO: test duplicates in result config list
# TODO: Interpolation support


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
    ],
)
def test_get_default_package(default: InputDefault, expected) -> None:
    assert default.get_default_package() == expected


@mark.parametrize(
    "default,expected",
    [
        # empty parent package
        param(
            ConfigDefault(path="bar", parent_package=""),
            "",
            id="config_default:path=bar,parent_package=,package=",
        ),
        param(
            ConfigDefault(path="group1/bar", parent_package=""),
            "group1",
            id="config_default:path=group1/bar,parent_package=, package=",
        ),
        param(
            ConfigDefault(path="bar", parent_package="", package="pkg1"),
            "pkg1",
            id="config_default:path=bar,parent_package=, package=pkg1",
        ),
        param(
            ConfigDefault(path="group1/bar", parent_package="", package="pkg1"),
            "pkg1",
            id="config_default:path=group1/bar,parent_package=,package=pkg1",
        ),
        # non empty parent package
        param(
            ConfigDefault(path="bar", parent_package="a", package="pkg1"),
            "a.pkg1",
            id="config_default:path=bar,parent_package=a, package=pkg1",
        ),
        # global package
        param(
            ConfigDefault(path="bar", parent_package="a", package="_global_.pkg1"),
            "pkg1",
            id="config_default:parent_package=a, package=_global_.pkg1",
        ),
        # global parent package
        param(
            ConfigDefault(path="bar", parent_package="_global_.foo", package="pkg1"),
            "foo.pkg1",
            id="config_default:parent_package=_global_.foo, package=pkg1",
        ),
        # both globals
        param(
            ConfigDefault(
                path="bar", parent_package="_global_.foo", package="_global_.pkg1"
            ),
            "pkg1",
            id="config_default:parent_package=_global_.foo, package=_global_.pkg1",
        ),
    ],
)
def test_get_final_package(default: InputDefault, expected) -> None:
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
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
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
                    config_path="config_default_pkg1", package="", is_self=True
                ),
                ResultDefault(
                    config_path="empty", package="pkg1", parent="config_default_pkg1"
                ),
            ],
            id="config_default_pkg1",
        ),
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
    ],
)
def test_override_package_in_defaults_list(
    config_name: str,
    overrides: List[str],
    expected: List[ResultDefault],
) -> None:
    _test_defaults_list_impl(
        config_name=config_name, overrides=overrides, expected=expected
    )
