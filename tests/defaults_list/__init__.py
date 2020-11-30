# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Any

from hydra._internal.config_repository import IConfigRepository, ConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.new_defaults_list import (
    DefaultsTreeNode,
    _create_defaults_tree,
    Overrides,
    _create_root,
)
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
) -> None:
    parser = OverridesParser.create()
    repo = create_repo()
    root = _create_root(config_name=config_name, with_hydra=prepend_hydra)
    overrides_list = parser.parse_overrides(overrides=input_overrides)
    overrides = Overrides(repo=repo, overrides_list=overrides_list)

    if isinstance(expected, DefaultsTreeNode):
        result = _create_defaults_tree(
            repo=repo,
            root=root,
            overrides=overrides,
            is_primary_config=True,
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
            )
            overrides.ensure_overrides_used()
