# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import mark, param
from typing import List

from hydra._internal.config_repository import ConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.NewDefaultElement import InputDefaultElement
from hydra.core.plugins import Plugins
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()

# registers config source plugins
Plugins.instance()


def create_repo():
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path="file://tests/test_data/default_lists")
    return ConfigRepository(config_search_path=csp)


@mark.parametrize(
    "config_path,expected_list",
    [
        param("empty", [], id="empty"),
        param(
            "one_item",
            [InputDefaultElement(group="group1", name="file1")],
            id="one_item",
        ),
        param(
            "one_item",
            [InputDefaultElement(group="group1", name="file1")],
            id="one_item",
        ),
        param(
            "self_leading",
            [
                InputDefaultElement(name="_self_"),
                InputDefaultElement(group="group1", name="file1"),
            ],
            id="self_leading",
        ),
        param(
            "self_trailing",
            [
                InputDefaultElement(group="group1", name="file1"),
                InputDefaultElement(name="_self_"),
            ],
            id="self_trailing",
        ),
        param(
            "optional",
            [
                InputDefaultElement(group="group1", name="file1", optional=True),
            ],
            id="optional",
        ),
        param(
            "non_config_group_default",
            [
                InputDefaultElement(name="some_config"),
            ],
            id="non_config_group_default",
        ),
    ],
)
def test_loaded_defaults_list(
    config_path: str, expected_list: List[InputDefaultElement]
):
    repo = create_repo()
    result = repo.load_config(config_path=config_path, is_primary_config=True)
    assert result.new_defaults_list == expected_list
