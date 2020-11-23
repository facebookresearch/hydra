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
from hydra.core.NewDefaultElement import InputDefault
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
            [InputDefault(group="group1", name="file1")],
            id="one_item",
        ),
        param(
            "one_item",
            [InputDefault(group="group1", name="file1")],
            id="one_item",
        ),
        param(
            "self_leading",
            [
                InputDefault(name="_self_"),
                InputDefault(group="group1", name="file1"),
            ],
            id="self_leading",
        ),
        param(
            "self_trailing",
            [
                InputDefault(group="group1", name="file1"),
                InputDefault(name="_self_"),
            ],
            id="self_trailing",
        ),
        param(
            "optional",
            [
                InputDefault(group="group1", name="file1", optional=True),
            ],
            id="optional",
        ),
        param(
            "non_config_group_default",
            [
                InputDefault(name="some_config"),
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
    parent = InputDefault(name=config_name)
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
            DefaultsTreeNode(parent=InputDefault(name="empty")),
            id="empty",
        ),
        param(
            "non_config_group_default",
            [],
            DefaultsTreeNode(
                parent=InputDefault(name="non_config_group_default"),
                children=[InputDefault(name="empty")],
            ),
            id="non_config_group_default",
        ),
        param(
            "one_item",
            [],
            DefaultsTreeNode(
                parent=InputDefault(name="one_item"),
                children=[InputDefault(group="group1", name="file1")],
            ),
            id="one_item",
        ),
        param(
            "optional",
            [],
            DefaultsTreeNode(
                parent=InputDefault(name="optional"),
                children=[
                    InputDefault(group="group1", name="file1", optional=True),
                ],
            ),
            id="optional",
        ),
        param(
            "self_leading",
            [],
            DefaultsTreeNode(
                parent=InputDefault(name="self_leading"),
                children=[
                    InputDefault(name="_self_"),
                    InputDefault(group="group1", name="file1"),
                ],
            ),
            id="self_leading",
        ),
        param(
            "self_trailing",
            [],
            DefaultsTreeNode(
                parent=InputDefault(name="self_trailing"),
                children=[
                    InputDefault(group="group1", name="file1"),
                    InputDefault(name="_self_"),
                ],
            ),
            id="self_trailing",
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
