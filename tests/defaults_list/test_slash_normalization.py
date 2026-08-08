# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import raises

from hydra import compose, initialize
from hydra._internal.defaults_list import create_defaults_list
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
    assert len(result_defaults) == 3

    # We verify that it resolved the config_path correctly:
    # "slash_normalization/group_a/sub_group/item"
    assert (
        result_defaults[1].config_path == "slash_normalization/group_a/sub_group/item"
    )


def test_slash_normalization_old_behavior_error() -> None:
    repo = create_repo()
    config_name = "slash_normalization/old_behavior_trigger"

    # Since the nested default 'nested_config' is placed in
    # 'slash_normalization/group_b/nested_config.yaml' (old behavior)
    # instead of 'slash_normalization/group_b/sub_group/nested_config.yaml' (new behavior),
    # this must trigger our migration error.
    expected_msg = (
        r"Could not load 'slash_normalization/group_b/sub_group/nested_config'\.\n"
        r"However, a config was found at 'slash_normalization/group_b/nested_config', "
        r"which indicates this application\n"
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


def test_slash_normalization_compose_equivalence() -> None:
    # Verify that shorthand "foo: bar/baz" and canonical "foo/bar: baz"
    # compose to identical output configs and resolve nested relative defaults
    with initialize(config_path="data/slash_normalization"):
        cfg_shorthand = compose(config_name="shorthand")
        cfg_canonical = compose(config_name="canonical")

        assert cfg_shorthand == cfg_canonical
        assert cfg_shorthand.group_a.sub_group.x == 42
        assert cfg_shorthand.group_a.sub_group.y == 100


def test_slash_normalization_compose_migration_error() -> None:
    # Verify the migration error is caught and raised normally during standard composition
    with initialize(config_path="data/slash_normalization"):
        with raises(
            ConfigCompositionException, match="deprecated slash-containing default"
        ):
            compose(config_name="old_behavior_trigger")


def test_slash_normalization_compose_override_key() -> None:
    # Verify command-line override key is normalized to 'group_a/sub_group'
    # and affects the composed config as expected
    with initialize(config_path="data/slash_normalization"):
        cfg = compose(config_name="shorthand", overrides=["group_a/sub_group=item"])
        assert cfg.group_a.sub_group.x == 42

        # Overriding a normalized shorthand with command line key group_a/sub_group
        cfg_override = compose(
            config_name="shorthand", overrides=["~group_a/sub_group"]
        )
        assert "group_a" not in cfg_override or "sub_group" not in cfg_override.group_a


def test_slash_normalization_compose_legal_substring() -> None:
    # Verify values containing ".." but not as a segment (e.g. sub..group) are normalized
    with initialize(config_path="data/slash_normalization"):
        cfg = compose(config_name="legal_substring")
        assert cfg.group_a.sub[""].group.val == 999


def test_slash_normalization_compose_deferred_interpolation() -> None:
    # Verify that a deferred Defaults List interpolation (e.g. group_a: ${prefix}/item)
    # is normalized early after its interpolation has been resolved
    with initialize(config_path="data/slash_normalization"):
        cfg = compose(config_name="deferred_interpolation")
        assert cfg.group_a.sub_group.x == 42
        assert cfg.group_a.sub_group.y == 100
