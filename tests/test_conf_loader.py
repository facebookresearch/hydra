# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import pkg_resources
import pytest
from omegaconf import OmegaConf

from hydra._internal.config_loader import ConfigLoader, consume_argument
from hydra.errors import MissingConfigException
from hydra.test_utils.test_utils import chdir_hydra_root, create_search_path

chdir_hydra_root()


@pytest.mark.parametrize(
    "path", ["hydra/test_utils/configs", "pkg://hydra.test_utils.configs"]
)
class TestConfigLoader:
    def test_load_configuration(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="config.yaml",
        )
        cfg = config_loader.load_configuration(overrides=["abc=123"])
        del cfg["hydra"]
        assert cfg == OmegaConf.create({"normal_yaml_config": True, "abc": 123})

    def test_load_with_missing_default(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="missing-default.yaml",
        )
        with pytest.raises(MissingConfigException):
            config_loader.load_configuration()

    def test_load_with_missing_optional_default(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="missing-optional-default.yaml",
        )
        cfg = config_loader.load_configuration()
        del cfg["hydra"]
        assert cfg == {}

    def test_load_with_optional_default(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="optional-default.yaml",
        )
        cfg = config_loader.load_configuration()
        del cfg["hydra"]
        assert cfg == dict(foo=10)

    def test_load_changing_group_in_default(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="optional-default.yaml",
        )
        cfg = config_loader.load_configuration(["group1=file2"])
        del cfg["hydra"]
        assert cfg == dict(foo=20)

    def test_load_adding_group_not_in_default(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="optional-default.yaml",
        )
        cfg = config_loader.load_configuration(["group2=file1"])
        del cfg["hydra"]
        assert cfg == dict(foo=10, bar=100)

    def test_change_run_dir_with_override(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="overriding_run_dir.yaml",
        )
        cfg = config_loader.load_configuration(overrides=["hydra.run.dir=abc"])
        assert cfg.hydra.run.dir == "abc"

    def test_change_run_dir_with_config(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="overriding_run_dir.yaml",
        )
        cfg = config_loader.load_configuration(overrides=[])
        assert cfg.hydra.run.dir == "cde"

    def test_load_strict(self, path):
        """
        Ensure that in strict mode we can override only things that are already in the config
        :return:
        """
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            config_file="compose.yaml",
            strict_cfg=True,
        )
        # Test that overriding existing things works in strict mode
        cfg = config_loader.load_configuration(overrides=["foo=ZZZ"])
        del cfg["hydra"]
        assert cfg == {"foo": "ZZZ", "bar": 100}

        # Test that accessing a key that is not there will fail
        with pytest.raises(KeyError):
            cfg.not_here

        # Test that bad overrides triggers the KeyError
        with pytest.raises(KeyError):
            config_loader.load_configuration(overrides=["f00=ZZZ"])

    def test_load_history(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
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
            ("missing-optional-default.yaml", path, "test"),
            ("foo/missing.yaml", None, None),
        ]

    def test_load_history_with_basic_launcher(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
            strict_cfg=False,
            config_file="custom_default_launcher.yaml",
        )
        config_loader.load_configuration(overrides=["hydra/launcher=basic"])

        assert config_loader.get_load_history() == [
            ("hydra.yaml", "pkg://hydra.conf", "hydra"),
            ("hydra/hydra_logging/default.yaml", "pkg://hydra.conf", "hydra"),
            ("hydra/job_logging/default.yaml", "pkg://hydra.conf", "hydra"),
            ("hydra/launcher/basic.yaml", "pkg://hydra.conf", "hydra"),
            ("hydra/sweeper/basic.yaml", "pkg://hydra.conf", "hydra"),
            ("hydra/output/default.yaml", "pkg://hydra.conf", "hydra"),
            ("custom_default_launcher.yaml", path, "test"),
        ]

    def test_load_yml_file(self, path):
        config_loader = ConfigLoader(
            config_search_path=create_search_path([path]),
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


def test_non_config_group_default():
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["hydra/test_utils/configs"]),
        strict_cfg=False,
        config_file="non_config_group_default.yaml",
    )
    config_loader.load_configuration()
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/default.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/launcher/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default.yaml", "pkg://hydra.conf", "hydra"),
        ("non_config_group_default.yaml", "hydra/test_utils/configs", "test"),
        ("some_config.yaml", "hydra/test_utils/configs", "test"),
    ]


@pytest.mark.parametrize(
    "dotlist, candidates, expected, remaining_list",
    [
        (["a=1", "b=2", "c=3"], ["a"], ("a", "1"), ["b=2", "c=3"]),
        (["aa=1", "a=2", "c=3"], ["a"], ("a", "2"), ["aa=1", "c=3"]),
        (["aa=1", "a=2", "c=3"], ["a", "aa"], ("aa", "1"), ["a=2", "c=3"]),
        (["aa=1", "a=2", "c=3"], ["a", "d"], ("a", "2"), ["aa=1", "c=3"]),
        (["a=1", "b=2", "c=3"], ["x"], (None, None), ["a=1", "b=2", "c=3"]),
    ],
)
def test_consume_arguments(dotlist, candidates, expected, remaining_list):
    res = consume_argument(dotlist, candidates)
    assert dotlist == remaining_list
    assert res == expected
