# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra.core.plugins import Plugins
from hydra.plugins.config_source import ConfigSource
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra_plugins.github_configsource import GitHubConfigSource


@pytest.mark.parametrize(
    "type_, path",
    [
        (
            GitHubConfigSource,
            "github://facebookresearch.hydra/tests/test_apps/config_source_test_configs?ref=master",
        ),
    ],
)
class TestCoreConfigSources(ConfigSourceTestSuite):
    pass


def test_discovery() -> None:
    # Test that this config source is discoverable when looking at config sources
    assert GitHubConfigSource.__name__ in [
        x.__name__ for x in Plugins.discover(ConfigSource)
    ]
