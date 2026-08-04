# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import raises

from hydra._internal.defaults_list import create_defaults_list
from hydra.core.default_element import GroupDefault
from hydra.core.plugins import Plugins
from hydra.errors import ConfigCompositionException
from tests.defaults_list import create_repo

Plugins.instance()


def test_slash_normalization_success() -> None:
    repo = create_repo()
    config_name = "slash_normalization/config"

    # We expect defaults list to contain:
    # GroupDefault(group="slash_normalization/group_a/sub_group", value="item")
    defaults_list = create_defaults_list(
        repo=repo,
        config_name=config_name,
        overrides_list=[],
        prepend_hydra=False,
        skip_missing=False,
    )

    # Let's verify the defaults list
    result_defaults = defaults_list.defaults
    assert len(result_defaults) == 2
    
    # We verify that it resolved the config_path correctly:
    # "slash_normalization/group_a/sub_group/item"
    assert result_defaults[0].config_path == "slash_normalization/group_a/sub_group/item"


def test_slash_normalization_old_behavior_error() -> None:
    repo = create_repo()
    config_name = "slash_normalization/old_behavior_trigger"

    # Since the nested default 'nested_config' is placed in
    # 'slash_normalization/group_b/nested_config.yaml' (old behavior)
    # instead of 'slash_normalization/group_b/sub_group/nested_config.yaml' (new behavior),
    # this must trigger our migration error.
    expected_msg = (
        r"Could not load 'slash_normalization/group_b/sub_group/nested_config'\.\n"
        r"However, a config was found at 'slash_normalization/group_b/nested_config', which indicates this application\n"
        r"relies on the deprecated slash-containing default option shorthand behavior\.\n"
        r"In Hydra 1.4, defaults list items like 'group_b: sub_group/\.\.\.' are\n"
        r"normalized early to 'group_b/sub_group: \.\.\.'\."
    )

    with raises(ConfigCompositionException, match=expected_msg):
        create_defaults_list(
            repo=repo,
            config_name=config_name,
            overrides_list=[],
            prepend_hydra=False,
            skip_missing=False,
        )
