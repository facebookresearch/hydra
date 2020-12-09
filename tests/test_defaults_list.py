# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from textwrap import dedent
from typing import Any, List

import pytest

from hydra._internal.config_repository import ConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.defaults_list import (
    compute_element_defaults_list,
    convert_overrides_to_defaults,
    expand_defaults_list,
)
from hydra.core import DefaultElement
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.errors import ConfigCompositionException, OverrideParseException
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()

# registers config source plugins
Plugins.instance()


@pytest.mark.parametrize(  # type: ignore
    "element,expected",
    [
        pytest.param(
            DefaultElement(config_name="no_defaults", parent="this_test"),
            [
                DefaultElement(config_name="no_defaults", parent="this_test"),
            ],
            id="no_defaults",
        ),
        pytest.param(
            DefaultElement(config_name="duplicate_self", parent="this_test"),
            pytest.raises(
                ConfigCompositionException,
                match="Duplicate _self_ defined in duplicate_self",
            ),
            id="duplicate_self",
        ),
        pytest.param(
            DefaultElement(config_name="trailing_self", parent="this_test"),
            [
                DefaultElement(config_name="no_defaults", parent="trailing_self"),
                DefaultElement(config_name="trailing_self", parent="this_test"),
            ],
            id="trailing_self",
        ),
        pytest.param(
            DefaultElement(config_name="implicit_leading_self", parent="this_test"),
            [
                DefaultElement(config_name="implicit_leading_self", parent="this_test"),
                DefaultElement(
                    config_name="no_defaults",
                    parent="implicit_leading_self",
                ),
            ],
            id="implicit_leading_self",
        ),
        pytest.param(
            DefaultElement(
                config_name="explicit_leading_self",
                parent="this_test",
            ),
            [
                DefaultElement(
                    config_name="explicit_leading_self",
                    parent="this_test",
                ),
                DefaultElement(
                    config_name="no_defaults",
                    parent="explicit_leading_self",
                ),
            ],
            id="explicit_leading_self",
        ),
        pytest.param(
            DefaultElement(config_name="a/a1"),
            [
                DefaultElement(config_name="a/a1"),
            ],
            id="primary_in_config_group_no_defaults",
        ),
        pytest.param(
            DefaultElement(config_group="a", config_name="a1"),
            [
                DefaultElement(config_group="a", config_name="a1"),
            ],
            id="primary_in_config_group_no_defaults",
        ),
        pytest.param(
            DefaultElement(config_name="a/global"),
            [
                DefaultElement(config_name="a/global"),
            ],
            id="a/global",
        ),
        pytest.param(
            DefaultElement(config_name="b/b1"),
            [
                DefaultElement(config_name="b/b1"),
            ],
            id="b/b1",
        ),
        pytest.param(
            DefaultElement(config_group="b", config_name="b1"),
            [
                DefaultElement(config_group="b", config_name="b1"),
            ],
            id="b/b1",
        ),
        pytest.param(
            DefaultElement(config_group="a", config_name="a2", parent="this_test"),
            [
                DefaultElement(config_group="a", config_name="a2", parent="this_test"),
                DefaultElement(config_group="b", config_name="b1", parent="a/a2"),
            ],
            id="a/a2",
        ),
        pytest.param(
            DefaultElement(
                config_name="recursive_item_explicit_self", parent="this_test"
            ),
            [
                DefaultElement(
                    config_name="recursive_item_explicit_self", parent="this_test"
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a2",
                    parent="recursive_item_explicit_self",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="a/a2",
                ),
            ],
            id="recursive_item_explicit_self",
        ),
        pytest.param(
            DefaultElement(
                config_name="recursive_item_explicit_self", parent="this_test"
            ),
            [
                DefaultElement(
                    config_name="recursive_item_explicit_self", parent="this_test"
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a2",
                    parent="recursive_item_explicit_self",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="a/a2",
                ),
            ],
            id="recursive_item_implicit_self",
        ),
        pytest.param(
            DefaultElement(config_group="a", config_name="a3", parent="this_test"),
            [
                DefaultElement(config_group="a", config_name="a3", parent="this_test"),
                DefaultElement(config_group="c", config_name="c2", parent="a/a3"),
                DefaultElement(config_group="b", config_name="b2", parent="a/a3"),
            ],
            id="multiple_item_definitions",
        ),
        pytest.param(
            DefaultElement(config_group="a", config_name="a4", parent="this_test"),
            [
                DefaultElement(config_group="a", config_name="a4", parent="this_test"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    package="file_pkg",
                    parent="a/a4",
                ),
            ],
            id="a/a4_pkg_override_in_config",
        ),
        pytest.param(
            DefaultElement(config_group="b", config_name="b3", parent="this_test"),
            [
                DefaultElement(config_group="b", config_name="b3", parent="this_test"),
            ],
            id="b/b3",
        ),
        pytest.param(
            DefaultElement(config_group="a", config_name="a5", parent="this_test"),
            [
                DefaultElement(config_group="a", config_name="a5", parent="this_test"),
                DefaultElement(config_group="b", config_name="b3", parent="a/a5"),
                DefaultElement(
                    config_group="b",
                    config_name="b3",
                    package="file_pkg",
                    parent="a/a5",
                ),
            ],
            id="a/a5",
        ),
        pytest.param(
            DefaultElement(
                config_group="b", config_name="base_from_a", parent="this_test"
            ),
            [
                DefaultElement(config_name="a/a1", parent="b/base_from_a"),
                DefaultElement(
                    config_group="b",
                    config_name="base_from_a",
                    parent="this_test",
                ),
            ],
            id="b/base_from_a",
        ),
        pytest.param(
            DefaultElement(
                config_group="b", config_name="base_from_b", parent="this_test"
            ),
            [
                DefaultElement(config_name="b/b1", parent="b/base_from_b"),
                DefaultElement(
                    config_group="b", config_name="base_from_b", parent="this_test"
                ),
            ],
            id="b/base_from_b",
        ),
        # rename
        pytest.param(
            DefaultElement(config_group="rename", config_name="r1", parent="this_test"),
            [
                DefaultElement(
                    config_group="rename", config_name="r1", parent="this_test"
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg",
                    config_name="b1",
                    parent="rename/r1",
                ),
            ],
            id="rename_package_from_none",
        ),
        pytest.param(
            DefaultElement(config_group="rename", config_name="r2", parent="this_test"),
            [
                DefaultElement(
                    config_group="rename", config_name="r2", parent="this_test"
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg2",
                    config_name="b1",
                    parent="rename/r2",
                ),
            ],
            id="rename_package_from_something",
        ),
        pytest.param(
            DefaultElement(config_group="rename", config_name="r3", parent="this_test"),
            [
                DefaultElement(
                    config_group="rename", config_name="r3", parent="this_test"
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg",
                    config_name="b4",
                    parent="rename/r3",
                ),
            ],
            id="rename_package_from_none_and_change_option:r3",
        ),
        pytest.param(
            DefaultElement(config_group="rename", config_name="r4", parent="this_test"),
            [
                DefaultElement(
                    config_group="rename",
                    config_name="r4",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg2",
                    config_name="b4",
                    parent="rename/r4",
                ),
            ],
            id="rename_package_and_change_option:r4",
        ),
        pytest.param(
            DefaultElement(config_group="rename", config_name="r5", parent="this_test"),
            [
                DefaultElement(
                    config_group="rename",
                    config_name="r5",
                    parent="this_test",
                ),
                DefaultElement(
                    config_name="rename/r4",
                    parent="rename/r5",
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg2",
                    config_name="b4",
                    parent="rename/r4",
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    parent="rename/r5",
                ),
            ],
            id="rename_package_and_change_option:r5",
        ),
        # delete
        pytest.param(
            DefaultElement(config_group="delete", config_name="d1", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete", config_name="d1", parent="this_test"
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="delete/d1",
                ),
            ],
            id="delete_with_null",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d2", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete", config_name="d2", parent="this_test"
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="delete/d2",
                ),
            ],
            id="delete_with_tilda",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d3", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete", config_name="d3", parent="this_test"
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="delete/d3",
                ),
            ],
            id="delete_with_tilda_k=v",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d4", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete",
                    config_name="d4",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="delete/d4",
                ),
            ],
            id="file_delete_not_mandatory",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d5", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete", config_name="d5", parent="this_test"
                ),
                DefaultElement(config_group="b", config_name="b1", parent="delete/d5"),
            ],
            id="file_delete_not_mandatory",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d7", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete", config_name="d7", parent="this_test"
                ),
                DefaultElement(config_group="b", config_name="b1", parent="delete/d7"),
            ],
            id="file_delete_not_mandatory",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d6", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete",
                    config_name="d6",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="delete/d6",
                ),
            ],
            id="specific_delete",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d8", parent="this_test"),
            [
                DefaultElement(
                    config_group="delete", config_name="d8", parent="this_test"
                ),
                DefaultElement(config_group="b", config_name="b2", parent="delete/d8"),
                DefaultElement(
                    config_group="c",
                    config_name="c2",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="b/b2",
                ),
            ],
            id="delete_from_included",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d9"),
            [
                DefaultElement(config_group="delete", config_name="d9"),
            ],
            id="file_delete_not_mandatory",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d11"),
            [
                DefaultElement(config_group="delete", config_name="d11"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="delete/d11",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg1",
                    config_name="b1",
                    parent="delete/d11",
                ),
            ],
            id="delete_is_specific",
        ),
        pytest.param(
            DefaultElement(config_group="delete", config_name="d12"),
            [
                DefaultElement(config_group="delete", config_name="d12"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="delete/d12",
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg1",
                    config_name="b1",
                    parent="delete/d12",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
            ],
            id="delete_is_specific",
        ),
        # interpolation
        pytest.param(
            DefaultElement(
                config_group="interpolation",
                config_name="i1",
                parent="this_test",
            ),
            [
                DefaultElement(
                    config_group="interpolation",
                    config_name="i1",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    parent="interpolation/i1",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="interpolation/i1",
                ),
                DefaultElement(
                    config_group="a_b",
                    config_name="a1_b1",
                    parent="interpolation/i1",
                ),
            ],
            id="interpolation",
        ),
        pytest.param(
            DefaultElement(
                config_group="interpolation",
                config_name="i2_legacy_with_self",
                parent="this_test",
            ),
            [
                DefaultElement(
                    config_group="interpolation",
                    config_name="i2_legacy_with_self",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    parent="interpolation/i2_legacy_with_self",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="interpolation/i2_legacy_with_self",
                ),
                DefaultElement(
                    config_group="a_b",
                    config_name="a1_b1",
                    parent="interpolation/i2_legacy_with_self",
                ),
            ],
            id="interpolation_legacy",
        ),
        pytest.param(
            DefaultElement(
                config_group="interpolation",
                config_name="i3_legacy_without_self",
                parent="this_test",
            ),
            [
                DefaultElement(
                    config_group="interpolation",
                    config_name="i3_legacy_without_self",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    parent="interpolation/i3_legacy_without_self",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="interpolation/i3_legacy_without_self",
                ),
                DefaultElement(
                    config_group="a_b",
                    config_name="a1_b1",
                    parent="interpolation/i3_legacy_without_self",
                ),
            ],
            id="interpolation_legacy",
        ),
        pytest.param(
            DefaultElement(
                config_group="interpolation",
                config_name="i4_forward",
                parent="this_test",
            ),
            [
                DefaultElement(
                    config_group="interpolation",
                    config_name="i4_forward",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="a_b",
                    config_name="a1_b1",
                    parent="interpolation/i4_forward",
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    parent="interpolation/i4_forward",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="interpolation/i4_forward",
                ),
            ],
            id="forward_interpolation",
        ),
        # optional
        pytest.param(
            DefaultElement(config_name="with_optional", parent="this_test"),
            [
                DefaultElement(config_name="with_optional", parent="this_test"),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    optional=True,
                    parent="with_optional",
                ),
                DefaultElement(
                    config_group="foo",
                    config_name="bar",
                    optional=True,
                    skip_load=True,
                    skip_load_reason="missing_optional_config",
                    parent="with_optional",
                ),
            ],
            id="optional",
        ),
        # missing
        pytest.param(
            DefaultElement(config_name="with_missing"),
            pytest.raises(
                ConfigCompositionException,
                match=dedent(
                    """\
                You must specify 'a', e.g, a=<OPTION>
                Available options:
                \ta1
                \ta2
                \ta3
                \ta4
                \ta5
                \ta6
                \tglobal"""
                ),
            ),
            id="missing",
        ),
        # delete renamed
        pytest.param(
            DefaultElement(config_group="delete_rename", config_name="dr1"),
            [
                DefaultElement(config_group="delete_rename", config_name="dr1"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="delete_rename/dr1",
                    package="pkg",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
            ],
            id="delete_src_after_rename_in_file",
        ),
        pytest.param(
            DefaultElement(config_group="delete_rename", config_name="dr2"),
            [
                DefaultElement(config_group="delete_rename", config_name="dr2"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="delete_rename/dr2",
                    package="pkg",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
            ],
            id="delete_dst_after_rename_in_file",
        ),
        # delete renamed
        pytest.param(
            DefaultElement(config_group="delete_rename", config_name="rd1"),
            [
                DefaultElement(config_group="delete_rename", config_name="rd1"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="delete_rename/rd1",
                    package="pkg",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
            ],
            id="rename_delete",
        ),
        pytest.param(
            DefaultElement(config_group="delete_rename", config_name="rd2"),
            [
                DefaultElement(config_group="delete_rename", config_name="rd2"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="delete_rename/rd2",
                    package="pkg",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
            ],
            id="rename_delete",
        ),
    ],
)
def test_compute_element_defaults_list(
    hydra_restore_singletons: Any,
    element: DefaultElement,
    expected: Any,
    recwarn: Any,
) -> None:

    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/new_defaults_lists")
    repo = ConfigRepository(config_search_path=csp)

    if isinstance(expected, list):
        ret = compute_element_defaults_list(
            element=element, skip_missing=False, repo=repo
        )
        assert ret == expected
    else:
        with expected:
            compute_element_defaults_list(
                element=element, skip_missing=False, repo=repo
            )


@pytest.mark.parametrize(  # type: ignore
    "input_defaults,expected",
    [
        pytest.param(
            [
                DefaultElement(config_group="a", config_name="a1", parent="foo"),
                DefaultElement(config_group="a", config_name="a6", parent="bar"),
            ],
            [
                DefaultElement(config_group="a", config_name="a6", parent="foo"),
            ],
            id="simple",
        ),
        pytest.param(
            [
                DefaultElement(config_group="a", config_name="a2", parent="foo"),
                DefaultElement(config_group="a", config_name="a6", parent="bar"),
            ],
            [
                DefaultElement(config_group="a", config_name="a6", parent="foo"),
            ],
            id="simple",
        ),
        pytest.param(
            [
                DefaultElement(config_group="a", config_name="a5", parent="foo"),
                DefaultElement(config_group="b", config_name="b1", parent="bar"),
                DefaultElement(
                    config_group="b",
                    package="file_pkg",
                    config_name="b1",
                    parent="zoo",
                ),
            ],
            [
                DefaultElement(config_group="a", config_name="a5", parent="foo"),
                DefaultElement(config_group="b", config_name="b1", parent="a/a5"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    package="file_pkg",
                    parent="a/a5",
                ),
            ],
            id="a/a5",
        ),
    ],
)
def test_expand_defaults_list(
    hydra_restore_singletons: Any,
    input_defaults: List[DefaultElement],
    expected: List[DefaultElement],
) -> None:
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/new_defaults_lists")
    repo = ConfigRepository(config_search_path=csp)

    ret = expand_defaults_list(defaults=input_defaults, skip_missing=False, repo=repo)
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "config_with_defaults,overrides,expected",
    [
        # change item
        pytest.param(
            "test_overrides",
            ["a=a6"],
            [
                DefaultElement(config_name="test_overrides", parent="this_test"),
                DefaultElement(
                    config_group="a",
                    config_name="a6",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="a",
                    package="pkg",
                    config_name="a1",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="c", config_name="c1", parent="test_overrides"
                ),
            ],
            id="change_option",
        ),
        # pytest.param(
        #     "test_overrides",
        #     ["a@:pkg2=a6"],
        #     [
        #         DefaultElement(config_name="test_overrides", parent="this_test"),
        #         DefaultElement(
        #             config_group="a",
        #             package="pkg2",
        #             config_name="a6",
        #             parent="test_overrides",
        #         ),
        #         DefaultElement(
        #             config_group="a",
        #             package="pkg",
        #             config_name="a1",
        #             parent="test_overrides",
        #         ),
        #         DefaultElement(
        #             config_group="c", config_name="c1", parent="test_overrides"
        #         ),
        #     ],
        #     id="change_both",
        # ),
        # pytest.param(
        #     "test_overrides",
        #     ["a@pkg:pkg2=a6"],
        #     [
        #         DefaultElement(config_name="test_overrides", parent="this_test"),
        #         DefaultElement(
        #             config_group="a", config_name="a1", parent="test_overrides"
        #         ),
        #         DefaultElement(
        #             config_group="a",
        #             package="pkg2",
        #             config_name="a6",
        #             parent="test_overrides",
        #         ),
        #         DefaultElement(
        #             config_group="c", config_name="c1", parent="test_overrides"
        #         ),
        #     ],
        #     id="change_both",
        # ),
        # pytest.param(
        #     "test_overrides",
        #     ["a@XXX:dest=a6"],
        #     pytest.raises(
        #         ConfigCompositionException,
        #         match=re.escape(
        #             "Could not rename package. No match for 'a@XXX' in the defaults list"
        #         ),
        #     ),
        #     id="change_both_invalid_package",
        # ),
        # adding item
        pytest.param(
            "no_defaults",
            ["+b=b1"],
            [
                DefaultElement(config_name="no_defaults", parent="this_test"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    is_add=True,
                    parent="overrides",
                ),
            ],
            id="adding_item",
        ),
        pytest.param(
            "no_defaults",
            ["+b=b2"],
            [
                DefaultElement(config_name="no_defaults", parent="this_test"),
                DefaultElement(config_group="b", config_name="b2", parent="overrides"),
                DefaultElement(config_group="c", config_name="c2", parent="b/b2"),
            ],
            id="adding_item_recursive",
        ),
        pytest.param(
            "test_overrides",
            ["+b@pkg=b1"],
            [
                DefaultElement(config_name="test_overrides", parent="this_test"),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="a",
                    package="pkg",
                    config_name="a1",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="c", config_name="c1", parent="test_overrides"
                ),
                DefaultElement(
                    config_group="b",
                    package="pkg",
                    config_name="b1",
                    is_add=True,
                    parent="overrides",
                ),
            ],
            id="adding_item_at_package",
        ),
        pytest.param(
            "one_missing_item",
            ["+a=a1"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not add 'a=a1'. 'a' is already in the defaults list."
                ),
            ),
            id="adding_duplicate_item",
        ),
        pytest.param(
            "test_overrides",
            ["+a=a2"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not add 'a=a2'. 'a' is already in the defaults list."
                ),
            ),
            id="adding_duplicate_item",
        ),
        pytest.param(
            "test_overrides",
            ["+a=a6", "+c=c2"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not add 'c=c2'. 'c' is already in the defaults list."
                ),
            ),
            id="adding_duplicate_item_recursive",
        ),
        # pytest.param(
        #     "test_overrides",
        #     ["+a@pkg:pkg2=a1"],
        #     pytest.raises(
        #         ConfigCompositionException,
        #         match=re.escape(
        #             "Add syntax does not support package rename, remove + prefix"
        #         ),
        #     ),
        #     id="add_rename_error",
        # ),
        pytest.param(
            "test_overrides",
            ["+a@pkg=a2"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not add 'a@pkg=a2'. 'a@pkg' is already in the defaults list."
                ),
            ),
            id="adding_duplicate_item@pkg",
        ),
        pytest.param(
            "no_defaults",
            ["c=c1"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not override 'c'. No match in the defaults list."
                    "\nTo append to your default list use +c=c1"
                ),
            ),
            id="adding_without_plus",
        ),
        # deleting item
        pytest.param(
            "no_defaults",
            ["~db=mysql"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not delete. No match for 'db=mysql' in the defaults list."
                ),
            ),
            id="delete_no_match",
        ),
        pytest.param(
            "no_defaults",
            ["~db"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not delete. No match for 'db' in the defaults list."
                ),
            ),
            id="delete_no_match",
        ),
        pytest.param(
            "no_defaults",
            ["~db=foo"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not delete. No match for 'db=foo' in the defaults list."
                ),
            ),
            id="delete_no_match",
        ),
        pytest.param(
            "test_overrides",
            ["~a"],
            [
                DefaultElement(config_name="test_overrides", parent="this_test"),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="a",
                    package="pkg",
                    config_name="a1",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="c", config_name="c1", parent="test_overrides"
                ),
            ],
            id="delete ~a",
        ),
        pytest.param(
            "test_overrides",
            ["~a=a1"],
            [
                DefaultElement(config_name="test_overrides", parent="this_test"),
                DefaultElement(
                    config_group="a",
                    config_name="a1",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="a",
                    package="pkg",
                    config_name="a1",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="c", config_name="c1", parent="test_overrides"
                ),
            ],
            id="delete ~a=a1",
        ),
        pytest.param(
            "no_defaults",
            ["~a=zzz"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not delete. No match for 'a=zzz' in the defaults list."
                ),
            ),
            id="delete ~a=zzz",
        ),
        pytest.param(
            "test_overrides",
            ["~a=zzz"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Could not delete. No match for 'a=zzz' in the defaults list."
                ),
            ),
            id="delete ~a=zzz",
        ),
        pytest.param(
            "test_overrides",
            ["~a@pkg"],
            [
                DefaultElement(config_name="test_overrides", parent="this_test"),
                DefaultElement(
                    config_group="a", config_name="a1", parent="test_overrides"
                ),
                DefaultElement(
                    config_group="a",
                    package="pkg",
                    config_name="a1",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="test_overrides",
                ),
                DefaultElement(
                    config_group="c", config_name="c1", parent="test_overrides"
                ),
            ],
            id="delete ~a@pkg",
        ),
        pytest.param(
            "no_defaults",
            ["a=foo", "~a"],
            [
                DefaultElement(config_name="no_defaults", parent="this_test"),
                DefaultElement(
                    config_group="a",
                    config_name="foo",
                    from_override=True,
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                    parent="overrides",
                ),
            ],
            id="delete_after_set_from_overrides",
        ),
        pytest.param(
            "a/a2",
            ["b=b2"],
            [
                DefaultElement(config_name="a/a2", parent="this_test"),
                DefaultElement(config_group="b", config_name="b2", parent="a/a2"),
                DefaultElement(config_group="c", config_name="c2", parent="b/b2"),
            ],
            id="delete_after_set_from_overrides:baseline",
        ),
        pytest.param(
            "a/a2",
            ["b=b2", "~b"],
            [
                DefaultElement(config_name="a/a2", parent="this_test"),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="a/a2",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
            ],
            id="delete_after_set_from_overrides",
        ),
        pytest.param(
            "a/a2",
            ["b=b2", "~c"],
            [
                DefaultElement(config_name="a/a2", parent="this_test"),
                DefaultElement(
                    config_group="b",
                    config_name="b2",
                    parent="a/a2",
                ),
                DefaultElement(
                    config_group="c",
                    config_name="c2",
                    parent="b/b2",
                    is_deleted=True,
                    skip_load=True,
                    skip_load_reason="deleted_from_list",
                ),
            ],
            id="delete_after_set_from_overrides",
        ),
        pytest.param(
            "delete/d10",
            ["b=b1"],
            [
                DefaultElement(config_name="delete/d10", parent="this_test"),
                DefaultElement(config_group="b", config_name="b1", parent="delete/d10"),
            ],
            id="override_deletion",
        ),
        pytest.param(
            "delete/d10",
            ["b=b1"],
            [
                DefaultElement(config_name="delete/d10", parent="this_test"),
                DefaultElement(config_group="b", config_name="b1", parent="delete/d10"),
            ],
            id="delete_overriden_2",
        ),
        # syntax error
        pytest.param(
            "test_overrides",
            ["db"],
            pytest.raises(
                OverrideParseException,
                match=re.escape(
                    "Error parsing override 'db'\nmissing EQUAL at '<EOF>'"
                ),
            ),
            id="syntax_error",
        ),
        pytest.param(
            "test_overrides",
            ["db=[a,b,c]"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Defaults list supported delete syntax is in the form "
                    "~group and ~group=value, where value is a group name (string)"
                ),
            ),
            id="syntax_error",
        ),
        pytest.param(
            "test_overrides",
            ["db={a:1,b:2}"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape(
                    "Defaults list supported delete syntax is in the form "
                    "~group and ~group=value, where value is a group name (string)"
                ),
            ),
            id="syntax_error",
        ),
        # interpolation
        pytest.param(
            "interpolation/i1",
            [],
            [
                DefaultElement(config_name="interpolation/i1", parent="this_test"),
                DefaultElement(
                    config_group="a", config_name="a1", parent="interpolation/i1"
                ),
                DefaultElement(
                    config_group="b", config_name="b1", parent="interpolation/i1"
                ),
                DefaultElement(
                    config_group="a_b", config_name="a1_b1", parent="interpolation/i1"
                ),
            ],
            id="interpolation",
        ),
        pytest.param(
            "interpolation/i1",
            ["a=a6"],
            [
                DefaultElement(config_name="interpolation/i1", parent="this_test"),
                DefaultElement(
                    config_group="a", config_name="a6", parent="interpolation/i1"
                ),
                DefaultElement(
                    config_group="b", config_name="b1", parent="interpolation/i1"
                ),
                DefaultElement(
                    config_group="a_b", config_name="a6_b1", parent="interpolation/i1"
                ),
            ],
            id="interpolation",
        ),
        pytest.param(
            "interpolation/i2_legacy_with_self",
            ["a=a6"],
            [
                DefaultElement(
                    config_name="interpolation/i2_legacy_with_self", parent="this_test"
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a6",
                    parent="interpolation/i2_legacy_with_self",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="interpolation/i2_legacy_with_self",
                ),
                DefaultElement(
                    config_group="a_b",
                    config_name="a6_b1",
                    parent="interpolation/i2_legacy_with_self",
                ),
            ],
            id="interpolation_legacy",
        ),
        pytest.param(
            "interpolation/i3_legacy_without_self",
            ["a=a6"],
            [
                DefaultElement(
                    config_name="interpolation/i3_legacy_without_self",
                    parent="this_test",
                ),
                DefaultElement(
                    config_group="a",
                    config_name="a6",
                    parent="interpolation/i3_legacy_without_self",
                ),
                DefaultElement(
                    config_group="b",
                    config_name="b1",
                    parent="interpolation/i3_legacy_without_self",
                ),
                DefaultElement(
                    config_group="a_b",
                    config_name="a6_b1",
                    parent="interpolation/i3_legacy_without_self",
                ),
            ],
            id="interpolation_legacy",
        ),
        # overriding groups with schema
        pytest.param(
            "config_with_schema",
            [],
            [
                DefaultElement(config_name="config_with_schema", parent="this_test"),
                DefaultElement(config_name="schema/c/c1", parent="c/c1_with_schema"),
                DefaultElement(
                    config_group="c",
                    config_name="c1_with_schema",
                    parent="config_with_schema",
                ),
            ],
            id="schema::no_override",
        ),
        pytest.param(
            "config_with_schema",
            # c1_with_schema is already the choice for c, should be no-op:
            ["c=c1_with_schema"],
            [
                DefaultElement(config_name="config_with_schema", parent="this_test"),
                DefaultElement(config_name="schema/c/c1", parent="c/c1_with_schema"),
                DefaultElement(
                    config_group="c",
                    config_name="c1_with_schema",
                    parent="config_with_schema",
                ),
            ],
            id="schema:override_to_same",
        ),
        pytest.param(
            "config_with_schema",
            ["c=c2_with_schema"],
            [
                DefaultElement(config_name="config_with_schema", parent="this_test"),
                DefaultElement(config_name="schema/c/c2", parent="c/c2_with_schema"),
                DefaultElement(
                    config_group="c",
                    config_name="c2_with_schema",
                    parent="config_with_schema",
                ),
            ],
            id="schema:override_to_c2_with_schema",
        ),
    ],
)
def test_apply_overrides_to_defaults(
    config_with_defaults: str,
    overrides: List[str],
    expected: Any,
    recwarn: Any,  # this tests some deprecated functionality
) -> None:
    assert isinstance(config_with_defaults, str)

    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/new_defaults_lists")
    repo = ConfigRepository(config_search_path=csp)

    def create_defaults() -> Any:
        parser = OverridesParser.create()
        parsed_overrides = parser.parse_overrides(overrides=overrides)
        overrides_as_defaults = convert_overrides_to_defaults(parsed_overrides)
        ret = [
            DefaultElement(config_name=config_with_defaults, parent="this_test"),
        ]
        ret.extend(overrides_as_defaults)
        return ret

    if isinstance(expected, list):
        defaults = create_defaults()
        ret = expand_defaults_list(defaults=defaults, skip_missing=False, repo=repo)
        assert ret == expected
    else:
        with expected:
            defaults = create_defaults()
            expand_defaults_list(defaults=defaults, skip_missing=False, repo=repo)


@pytest.mark.parametrize(  # type: ignore
    "element,expected",
    [
        pytest.param(
            DefaultElement(config_name="with_missing", parent="this_test"),
            [
                DefaultElement(config_name="with_missing", parent="this_test"),
                DefaultElement(
                    config_group="a",
                    config_name="???",
                    skip_load=True,
                    skip_load_reason="missing_skipped",
                    parent="with_missing",
                ),
            ],
            id="with_missing",
        ),
    ],
)
def test_missing_with_skip_missing(
    hydra_restore_singletons: Any,
    element: DefaultElement,
    expected: Any,
) -> None:

    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/new_defaults_lists")
    repo = ConfigRepository(config_search_path=csp)

    ret = compute_element_defaults_list(element=element, skip_missing=True, repo=repo)
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "element",
    [
        pytest.param(
            DefaultElement(
                config_group="interpolation", config_name="i2_legacy_with_self"
            ),
        ),
    ],
)
def test_legacy_interpolation_are_deprecated(
    hydra_restore_singletons: Any,
    element: DefaultElement,
) -> None:
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/new_defaults_lists")
    repo = ConfigRepository(config_search_path=csp)
    msg = dedent(
        """
        Defaults list element 'a_b=${defaults.1.a}_${defaults.2.b}' is using a deprecated interpolation form.
        See http://hydra.cc/docs/next/upgrades/1.0_to_1.1/defaults_list_interpolation for migration information.
        """
    )
    with pytest.warns(UserWarning, match=re.escape(msg)):
        compute_element_defaults_list(element=element, skip_missing=True, repo=repo)


@pytest.mark.parametrize(  # type: ignore
    "element",
    [
        pytest.param(
            DefaultElement(config_group="a", config_name="invalid_defaults_list"),
        ),
    ],
)
def test_load_invalid_defaults(
    hydra_restore_singletons: Any,
    element: DefaultElement,
) -> None:
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/new_defaults_lists")
    repo = ConfigRepository(config_search_path=csp)
    msg = dedent(
        f"""\
        Invalid defaults list in '{element.config_path()}', defaults must be a list.
        Example of a valid defaults:
        defaults:
          - dataset: imagenet
          - model: alexnet
            optional: true
          - optimizer: nesterov
        """
    )
    with pytest.raises(ValueError, match=re.escape(msg)):
        compute_element_defaults_list(element=element, skip_missing=True, repo=repo)
