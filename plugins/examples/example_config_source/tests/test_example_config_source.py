# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest
from omegaconf import OmegaConf

from hydra._internal.plugins import Plugins
from hydra.plugins.config import ConfigSource
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra_plugins.example_config_source.config_source_example import (
    ConfigSourceExample,
    ConfigStore,
)

# Setup config source for test
store = ConfigStore.instance()
store.mkdir("dataset")
store.mkdir("optimizer")

store.add(
    "dataset",
    "imagenet.yaml",
    OmegaConf.create({"dataset": {"name": "imagenet", "path": "/datasets/imagenet"}}),
)

store.add(
    "dataset",
    "cifar10.yaml",
    OmegaConf.create({"dataset": {"name": "cifar10", "path": "/datasets/cifar10"}}),
)


store.add(
    path="dataset",
    name="config_without_extension",
    node=OmegaConf.create({"foo": "bar"}),
)
store.add(
    path="", name="config_without_group.yaml", node=OmegaConf.create({"group": False}),
)


@pytest.mark.parametrize(
    "type_, path", [(ConfigSourceExample, "example://some_path")],
)
class TestCoreConfigSources(ConfigSourceTestSuite):
    pass


def test_discovery() -> None:
    # This may seem weird, but it verifies that we can discover this Plugin via
    # the plugins subsystem.
    # The discover method takes a class and return all plugins that implements that class.
    # Typically we would be discovering all plugins that implementing some common interface.
    plugins = Plugins.discover(ConfigSource)
    # discovered plugins are actually different class objects, compare by name
    assert ConfigSourceExample.__name__ in [x.__name__ for x in plugins]
