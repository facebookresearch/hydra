# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import create_search_path
from hydra._internal.config_loader import ConfigLoader
from hydra.errors import MissingConfigException
from hydra.test_utils.test_utils import chdir_hydra_root
import pkg_resources

chdir_hydra_root()


def test_override_run_dir_without_hydra_cfg():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(), strict_cfg=False, config_file=None
    )
    cfg = config_loader.load_configuration(overrides=["hydra.run.dir=abc"])
    assert cfg.hydra.run.dir == "abc"


def test_override_run_dir_with_hydra_cfg():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(
            ["demos/99_hydra_configuration/workdir/"]
        ),
        strict_cfg=False,
        config_file=None,
    )
    cfg = config_loader.load_configuration(overrides=["hydra.run.dir=abc"])
    assert cfg.hydra.run.dir == "abc"


def test_load_configuration():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["demos/3_config_file"]),
        strict_cfg=False,
        config_file="config.yaml",
    )
    cfg = config_loader.load_configuration(overrides=["abc=123"])
    del cfg["hydra"]
    assert cfg == OmegaConf.create(
        dict(abc=123, dataset=dict(name="imagenet", path="/datasets/imagenet"))
    )


def test_load_with_missing_default():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="missing-default.yaml",
    )
    with pytest.raises(MissingConfigException):
        config_loader.load_configuration()


def test_load_with_missing_optional_default():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="missing-optional-default.yaml",
    )
    cfg = config_loader.load_configuration()
    del cfg["hydra"]
    assert cfg == {}


def test_load_with_optional_default():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="optional-default.yaml",
    )
    cfg = config_loader.load_configuration()
    del cfg["hydra"]
    assert cfg == dict(foo=10)


def test_load_changing_group_in_default():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="optional-default.yaml",
    )
    cfg = config_loader.load_configuration(["group1=file2"])
    del cfg["hydra"]
    assert cfg == dict(foo=20)


def test_load_adding_group_not_in_default():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="optional-default.yaml",
    )
    cfg = config_loader.load_configuration(["group2=file1"])
    del cfg["hydra"]
    assert cfg == dict(foo=10, bar=100)


def test_load_history():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="missing-optional-default.yaml",
    )
    config_loader.load_configuration()
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/launcher/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default.yaml", "pkg://hydra.conf", "hydra"),
        ("missing-optional-default.yaml", "hydra/test_utils/configs", "test"),
        ("foo/missing.yaml", None, None),
    ]


def test_load_history_with_basic_launcher():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["demos/6_sweep/conf"]),
        strict_cfg=False,
        config_file="config.yaml",
    )
    config_loader.load_configuration(overrides=["hydra/launcher=basic"])

    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/launcher/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default.yaml", "pkg://hydra.conf", "hydra"),
        ("config.yaml", "demos/6_sweep/conf", "test"),
        ("optimizer/nesterov.yaml", "demos/6_sweep/conf", "test"),
    ]


def test_load_strict():
    """
    Ensure that in strict mode we can override only things that are already in the config
    :return:
    """
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["demos/3_config_file"]),
        config_file="config.yaml",
        strict_cfg=True,
    )
    cfg = config_loader.load_configuration(overrides=["dataset.name=foobar"])
    del cfg["hydra"]
    assert cfg == dict(dataset=dict(name="foobar", path="/datasets/imagenet"))
    with pytest.raises(KeyError):
        cfg.not_here

    with pytest.raises(KeyError):
        cfg.dataset.not_here

    config_loader = ConfigLoader(
        config_search_path=create_search_path(["demos/3_config_file"]),
        config_file="config.yaml",
        strict_cfg=True,
    )
    with pytest.raises(KeyError):
        config_loader.load_configuration(overrides=["dataset.bad_key=foobar"])


def test_load_yml_file():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="config.yml",
    )
    cfg = config_loader.load_configuration()
    del cfg["hydra"]
    assert cfg == dict(yml_file_here=True)


@pytest.mark.parametrize(
    "primary,merged,result",
    [
        ([], [], []),
        ([{"a": 10}], [], [{"a": 10}]),
        ([{"a": 10}, {"b": 20}], [{"a": 20}], [{"a": 20}, {"b": 20}]),
        (
            [
                {"hydra_logging": "default"},
                {"job_logging": "default"},
                {"launcher": "basic"},
                {"sweeper": "basic"},
            ],
            [{"optimizer": "nesterov"}, {"launcher": "basic"}],
            [
                {"hydra_logging": "default"},
                {"job_logging": "default"},
                {"launcher": "basic"},
                {"sweeper": "basic"},
                {"optimizer": "nesterov"},
            ],
        ),
    ],
)
def test_merge_default_lists(primary, merged, result):
    ConfigLoader._merge_default_lists(primary, merged)
    assert primary == result


@pytest.mark.parametrize(
    "config_file, overrides",
    [
        # remove from config
        ("removing-hydra-launcher-default.yaml", []),
        # remove from override
        ("config.yaml", ["hydra/launcher=null"]),
        # remove from both
        ("removing-hydra-launcher-default.yaml", ["hydra/launcher=null"]),
        # second overrides removes
        ("config.yaml", ["hydra/launcher=submitit", "hydra/launcher=null"]),
    ],
)
def test_default_removal(config_file, overrides):
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file=config_file,
    )
    config_loader.load_configuration(overrides=overrides)
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default.yaml", "pkg://hydra.conf", "hydra"),
        (config_file, "hydra/test_utils/configs", "test"),
    ]


def test_defaults_not_list_exception():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="defaults_not_list.yaml",
    )
    with pytest.raises(ValueError):
        config_loader.load_configuration(overrides=[])


@pytest.mark.parametrize(
    "module_name, resource_name",
    [
        ("hydra.test_utils", ""),
        ("hydra.test_utils", "__init__.py"),
        ("hydra.test_utils", "configs"),
        ("hydra.test_utils", "configs/config.yaml"),
        ("hydra.test_utils.configs", ""),
        ("hydra.test_utils.configs", "config.yaml"),
        ("hydra.test_utils.configs", "group1"),
        ("hydra.test_utils.configs", "group1/file1.yaml"),
    ],
)
def test_resource_exists(module_name, resource_name):
    assert pkg_resources.resource_exists(module_name, resource_name) is True


def test_override_hydra_config_value_from_config_file():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="overriding_output_dir.yaml",
    )

    cfg = config_loader.load_configuration(overrides=[])
    assert cfg.hydra.run.dir == "foo"


def test_override_hydra_config_group_from_config_file():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="overriding_logging_default.yaml",
    )

    config_loader.load_configuration(overrides=[])
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/hydra_debug.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/disabled.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default.yaml", "pkg://hydra.conf", "hydra"),
        ("overriding_logging_default.yaml", "hydra/test_utils/configs", "test"),
    ]


def test_list_groups():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="overriding_output_dir.yaml",
    )
    assert sorted(config_loader.list_groups("")) == [
        "completion_test",
        "group1",
        "group2",
        "hydra",
    ]

    assert sorted(config_loader.list_groups("hydra")) == [
        "hydra_logging",
        "job_logging",
        "launcher",
        "output",
        "sweeper",
    ]
