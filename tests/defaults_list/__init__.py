# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, List

from hydra._internal.config_repository import ConfigRepository, IConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.new_defaults_list import (
    Overrides,
    _create_defaults_tree,
    _create_root,
)
from hydra.core.new_default_element import DefaultsTreeNode
from hydra.core.override_parser.overrides_parser import OverridesParser


def create_repo() -> IConfigRepository:
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/default_lists")
    return ConfigRepository(config_search_path=csp)


def _test_defaults_tree_impl(
    config_name: str,
    input_overrides: List[str],
    expected: Any,
    prepend_hydra: bool = False,
    skip_missing: bool = False,
) -> None:
    parser = OverridesParser.create()
    repo = create_repo()
    root = _create_root(config_name=config_name, with_hydra=prepend_hydra)
    overrides_list = parser.parse_overrides(overrides=input_overrides)
    overrides = Overrides(repo=repo, overrides_list=overrides_list)

    if expected is None or isinstance(expected, DefaultsTreeNode):
        result = _create_defaults_tree(
            repo=repo,
            root=root,
            overrides=overrides,
            is_primary_config=True,
            interpolated_subtree=False,
            skip_missing=skip_missing,
        )
        overrides.ensure_overrides_used()
        assert result == expected
    else:
        with expected:
            _create_defaults_tree(
                repo=repo,
                root=root,
                overrides=overrides,
                is_primary_config=True,
                interpolated_subtree=False,
                skip_missing=skip_missing,
            )
            overrides.ensure_overrides_used()
