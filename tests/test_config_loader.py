# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any, List

import pkg_resources
import pytest
from omegaconf import MISSING, ListConfig, OmegaConf, ValidationError

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.utils import create_config_search_path
from hydra.core.config_store import SchemaStore
from hydra.errors import MissingConfigException
from hydra.test_utils.test_utils import (  # noqa: F401
    chdir_hydra_root,
    restore_singletons,
)

chdir_hydra_root()


@pytest.mark.parametrize(
    "path", ["file://hydra/test_utils/configs", "pkg://hydra.test_utils.configs"]
)
class TestConfigLoader:
    def test_load_configuration(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yaml", strict=False, overrides=["abc=123"]
        )
        del cfg["hydra"]
        assert cfg == {"normal_yaml_config": True, "abc": 123}

    def test_load_with_missing_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        with pytest.raises(MissingConfigException):
            config_loader.load_configuration(
                config_name="missing-default.yaml", overrides=[], strict=False
            )

    def test_load_with_missing_optional_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="missing-optional-default.yaml", overrides=[], strict=False
        )
        del cfg["hydra"]
        assert cfg == {}

    def test_load_with_optional_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml", overrides=[], strict=False
        )
        del cfg["hydra"]
        assert cfg == dict(foo=10)

    def test_load_changing_group_in_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml",
            overrides=["group1=file2"],
            strict=False,
        )
        del cfg["hydra"]
        assert cfg == dict(foo=20)

    def test_load_adding_group_not_in_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml",
            overrides=["group2=file1"],
            strict=False,
        )
        del cfg["hydra"]
        assert cfg == dict(foo=10, bar=100)

    def test_change_run_dir_with_override(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="overriding_run_dir.yaml",
            overrides=["hydra.run.dir=abc"],
            strict=False,
        )
        assert cfg.hydra.run.dir == "abc"

    def test_change_run_dir_with_config(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="overriding_run_dir.yaml", overrides=[], strict=False
        )
        assert cfg.hydra.run.dir == "cde"

    def test_load_strict(self, path: str) -> None:
        """
        Ensure that in strict mode we can override only things that are already in the config
        :return:
        """
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        # Test that overriding existing things works in strict mode
        cfg = config_loader.load_configuration(
            config_name="compose.yaml", overrides=["foo=ZZZ"], strict=True
        )
        del cfg["hydra"]
        assert cfg == {"foo": "ZZZ", "bar": 100}

        # Test that accessing a key that is not there will fail
        with pytest.raises(AttributeError):
            # noinspection PyStatementEffect
            cfg.not_here

        # Test that bad overrides triggers the KeyError
        with pytest.raises(KeyError):
            config_loader.load_configuration(
                config_name="compose.yaml", overrides=["f00=ZZZ"], strict=True
            )

    def test_load_history(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        config_loader.load_configuration(
            config_name="missing-optional-default.yaml", overrides=[], strict=False
        )
        assert config_loader.get_load_history() == [
            ("hydra.yaml", "pkg://hydra.conf", "hydra"),
            ("hydra/hydra_logging/default", "pkg://hydra.conf", "hydra"),
            ("hydra/job_logging/default", "pkg://hydra.conf", "hydra"),
            ("hydra/launcher/basic", "pkg://hydra.conf", "hydra"),
            ("hydra/sweeper/basic", "pkg://hydra.conf", "hydra"),
            ("hydra/output/default", "pkg://hydra.conf", "hydra"),
            ("hydra/help/default", "pkg://hydra.conf", "hydra"),
            ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra"),
            ("missing-optional-default.yaml", path, "main"),
            ("foo/missing", None, None),
        ]

    def test_load_history_with_basic_launcher(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        config_loader.load_configuration(
            config_name="custom_default_launcher.yaml",
            overrides=["hydra/launcher=basic"],
            strict=False,
        )

        assert config_loader.get_load_history() == [
            ("hydra.yaml", "pkg://hydra.conf", "hydra"),
            ("hydra/hydra_logging/default", "pkg://hydra.conf", "hydra"),
            ("hydra/job_logging/default", "pkg://hydra.conf", "hydra"),
            ("hydra/launcher/basic", "pkg://hydra.conf", "hydra"),
            ("hydra/sweeper/basic", "pkg://hydra.conf", "hydra"),
            ("hydra/output/default", "pkg://hydra.conf", "hydra"),
            ("hydra/help/default", "pkg://hydra.conf", "hydra"),
            ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra"),
            ("custom_default_launcher.yaml", path, "main"),
        ]

    def test_load_yml_file(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yml", overrides=[], strict=False
        )
        del cfg["hydra"]
        assert cfg == dict(yml_file_here=True)

    def test_override_with_equals(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yaml", overrides=["abc='cde=12'"], strict=False
        )
        del cfg["hydra"]
        assert cfg == OmegaConf.create({"normal_yaml_config": True, "abc": "cde=12"})

    def test_compose_file_with_dot(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="compose.yaml", overrides=["group1=abc.cde"], strict=False
        )
        del cfg["hydra"]
        assert cfg == {"abc=cde": None, "bar": 100}

    def test_load_with_schema(
        self, restore_singletons: Any, path: str  # noqa: F811
    ) -> None:
        @dataclass
        class MySQLConfig:
            driver: str = MISSING
            host: str = MISSING
            port: int = MISSING
            user: str = MISSING
            password: str = MISSING

        SchemaStore.instance().store(
            group="db", name="mysql", node=MySQLConfig, path="db"
        )

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )

        cfg = config_loader.load_configuration(config_name="db/mysql", overrides=[])
        del cfg["hydra"]
        assert cfg == {
            "db": {
                "driver": "mysql",
                "host": "???",
                "port": "???",
                "user": "omry",
                "password": "secret",
            }
        }

        cfg = config_loader.load_configuration(
            config_name="db/mysql", overrides=["db.port=101010"]
        )
        del cfg["hydra"]
        assert cfg == {
            "db": {
                "driver": "mysql",
                "host": "???",
                "port": 101010,
                "user": "omry",
                "password": "secret",
            }
        }

        with pytest.raises(ValidationError):
            config_loader.load_configuration(
                config_name="db/mysql", overrides=["db.port=fail"]
            )


@pytest.mark.parametrize(  # type:ignore
    "in_primary,in_merged,expected",
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
def test_merge_default_lists(
    in_primary: List[Any], in_merged: List[Any], expected: List[Any]
) -> None:
    primary = OmegaConf.create(in_primary)
    merged = OmegaConf.create(in_merged)
    assert isinstance(primary, ListConfig)
    assert isinstance(merged, ListConfig)
    ConfigLoaderImpl._merge_default_lists(primary, merged)
    assert primary == expected


@pytest.mark.parametrize(  # type:ignore
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
def test_default_removal(config_file: str, overrides: List[str]) -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )
    config_loader.load_configuration(
        config_name=config_file, overrides=overrides, strict=False
    )
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/default", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/default", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default", "pkg://hydra.conf", "hydra"),
        ("hydra/help/default", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra"),
        (config_file, "file://hydra/test_utils/configs", "main"),
    ]


def test_defaults_not_list_exception() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )
    with pytest.raises(ValueError):
        config_loader.load_configuration(
            config_name="defaults_not_list.yaml", overrides=[], strict=False
        )


@pytest.mark.parametrize(  # type:ignore
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
def test_resource_exists(module_name: str, resource_name: str) -> None:
    assert pkg_resources.resource_exists(module_name, resource_name) is True


def test_override_hydra_config_value_from_config_file() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )

    cfg = config_loader.load_configuration(
        config_name="overriding_output_dir.yaml", overrides=[], strict=False
    )
    assert cfg.hydra.run.dir == "foo"


def test_override_hydra_config_group_from_config_file() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )

    config_loader.load_configuration(
        config_name="overriding_logging_default.yaml", overrides=[], strict=False
    )
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/hydra_debug", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/disabled", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default", "pkg://hydra.conf", "hydra"),
        ("hydra/help/default", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra"),
        ("overriding_logging_default.yaml", "file://hydra/test_utils/configs", "main"),
    ]


def test_list_groups() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path(
            "hydra/test_utils/configs/cloud_infra_example"
        )
    )
    groups = config_loader.list_groups("")
    assert sorted(groups) == [
        "application",
        "cloud_provider",
        "db",
        "environment",
        "hydra",
    ]

    assert sorted(config_loader.list_groups("hydra")) == [
        "help",
        "hydra_help",
        "hydra_logging",
        "job_logging",
        "launcher",
        "output",
        "sweeper",
    ]


def test_non_config_group_default() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )
    config_loader.load_configuration(
        config_name="non_config_group_default.yaml", overrides=[], strict=False
    )
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/default", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/default", "pkg://hydra.conf", "hydra"),
        ("hydra/launcher/basic", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default", "pkg://hydra.conf", "hydra"),
        ("hydra/help/default", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra"),
        ("non_config_group_default.yaml", "file://hydra/test_utils/configs", "main"),
        ("some_config", "file://hydra/test_utils/configs", "main"),
    ]


def test_mixed_composition_order() -> None:
    """
    Tests that the order of mixed composition (defaults contains both config group and non config group
    items) is correct
    """
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )
    config_loader.load_configuration(
        config_name="mixed_compose.yaml", overrides=[], strict=False
    )
    assert config_loader.get_load_history() == [
        ("hydra.yaml", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_logging/default", "pkg://hydra.conf", "hydra"),
        ("hydra/job_logging/default", "pkg://hydra.conf", "hydra"),
        ("hydra/launcher/basic", "pkg://hydra.conf", "hydra"),
        ("hydra/sweeper/basic", "pkg://hydra.conf", "hydra"),
        ("hydra/output/default", "pkg://hydra.conf", "hydra"),
        ("hydra/help/default", "pkg://hydra.conf", "hydra"),
        ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra"),
        ("mixed_compose.yaml", "file://hydra/test_utils/configs", "main"),
        ("some_config", "file://hydra/test_utils/configs", "main"),
        ("group1/file1", "file://hydra/test_utils/configs", "main"),
        ("config", "file://hydra/test_utils/configs", "main"),
    ]
