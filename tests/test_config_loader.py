# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

import pkg_resources
import pytest
from omegaconf import MISSING, ListConfig, OmegaConf, ValidationError

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.utils import create_config_search_path
from hydra.core.config_store import ConfigStore, ConfigStoreWithProvider
from hydra.errors import MissingConfigException

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import (  # noqa: F401
    chdir_hydra_root,
    restore_singletons,
)

chdir_hydra_root()


@dataclass
class MySQLConfig:
    driver: str = MISSING
    host: str = MISSING
    port: int = MISSING
    user: str = MISSING
    password: str = MISSING


hydra_load_list: List[Tuple[str, Optional[str], Optional[str], Optional[str]]] = [
    ("hydra_config", "structured://", "hydra", None),
    ("hydra/hydra_logging/default", "pkg://hydra.conf", "hydra", None),
    ("hydra/job_logging/default", "pkg://hydra.conf", "hydra", None),
    ("hydra/launcher/basic", "pkg://hydra.conf", "hydra", None),
    (
        "hydra/sweeper/basic",
        "structured://",
        "hydra._internal.core_plugins.basic_sweeper",
        None,
    ),
    ("hydra/output/default", "pkg://hydra.conf", "hydra", None),
    ("hydra/help/default", "pkg://hydra.conf", "hydra", None),
    ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra", None),
]


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
        with pytest.raises(AttributeError):
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
        expected = hydra_load_list.copy()
        expected.append(("missing-optional-default.yaml", path, "main", None))
        expected.append(("foo/missing", None, None, None))

        assert config_loader.get_load_history() == expected

    def test_load_history_with_basic_launcher(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        config_loader.load_configuration(
            config_name="custom_default_launcher.yaml",
            overrides=["hydra/launcher=basic"],
            strict=False,
        )

        expected = hydra_load_list.copy()
        expected.append(("custom_default_launcher.yaml", path, "main", None))
        assert config_loader.get_load_history() == expected

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

    def test_load_config_with_schema(
        self, restore_singletons: Any, path: str  # noqa: F811
    ) -> None:

        ConfigStore.instance().store(
            group="db",
            name="mysql",
            node=MySQLConfig,
            path="db",
            provider="test_provider",
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

        expected = hydra_load_list.copy()
        expected.append(("db/mysql", path, "main", "test_provider"))
        assert config_loader.get_load_history() == expected

        # verify illegal modification is rejected at runtime
        with pytest.raises(ValidationError):
            cfg.db.port = "fail"

        # verify illegal override is rejected during load
        with pytest.raises(ValidationError):
            config_loader.load_configuration(
                config_name="db/mysql", overrides=["db.port=fail"]
            )

    def test_load_config_file_with_schema_validation(
        self, restore_singletons: Any, path: str  # noqa: F811
    ) -> None:

        with ConfigStoreWithProvider("test_provider") as config_store:
            config_store.store(group="db", name="mysql", node=MySQLConfig, path="db")

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="db/mysql", overrides=[], strict=False
        )

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

        expected = hydra_load_list.copy()
        expected.append(("db/mysql", path, "main", "test_provider"))
        assert config_loader.get_load_history() == expected


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

    expected = list(
        filter(lambda x: x[0] != "hydra/launcher/basic", hydra_load_list.copy())
    )
    expected.extend([(config_file, "file://hydra/test_utils/configs", "main", None)])
    assert config_loader.get_load_history() == expected


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

    # This load history is too different to easily reuse the standard hydra_load_list
    assert config_loader.get_load_history() == [
        ("hydra_config", "structured://", "hydra", None),
        ("hydra/hydra_logging/hydra_debug", "pkg://hydra.conf", "hydra", None),
        ("hydra/job_logging/disabled", "pkg://hydra.conf", "hydra", None),
        (
            "hydra/sweeper/basic",
            "structured://",
            "hydra._internal.core_plugins.basic_sweeper",
            None,
        ),
        ("hydra/output/default", "pkg://hydra.conf", "hydra", None),
        ("hydra/help/default", "pkg://hydra.conf", "hydra", None),
        ("hydra/hydra_help/default", "pkg://hydra.conf", "hydra", None),
        (
            "overriding_logging_default.yaml",
            "file://hydra/test_utils/configs",
            "main",
            None,
        ),
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

    expected = hydra_load_list.copy()
    expected.extend(
        [
            (
                "non_config_group_default.yaml",
                "file://hydra/test_utils/configs",
                "main",
                None,
            ),
            ("some_config", "file://hydra/test_utils/configs", "main", None),
        ]
    )
    assert config_loader.get_load_history() == expected


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

    expected = hydra_load_list.copy()
    expected.extend(
        [
            ("mixed_compose.yaml", "file://hydra/test_utils/configs", "main", None),
            ("some_config", "file://hydra/test_utils/configs", "main", None),
            ("group1/file1", "file://hydra/test_utils/configs", "main", None),
            ("config", "file://hydra/test_utils/configs", "main", None),
        ]
    )

    assert config_loader.get_load_history() == expected


def test_load_schema_as_config(restore_singletons: Any) -> None:  # noqa: F811
    """
    Load structured config as a configuration
    """
    ConfigStore.instance().store(
        group="db", name="mysql", node=MySQLConfig, path="db", provider="test_provider"
    )

    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    cfg = config_loader.load_configuration(config_name="db/mysql", overrides=[])
    del cfg["hydra"]
    assert cfg == {
        "db": {
            "driver": MISSING,
            "host": MISSING,
            "port": MISSING,
            "user": MISSING,
            "password": MISSING,
        }
    }

    expected = hydra_load_list.copy()
    expected.extend([("db/mysql", "structured://", "test_provider", None)])
    assert config_loader.get_load_history() == expected


@dataclass
class Plugin:
    name: str = MISSING
    params: Any = MISSING


@dataclass
class ConcretePlugin(Plugin):
    name: str = "foobar_plugin"

    @dataclass
    class FoobarParams:
        foo: int = 10

    params: FoobarParams = FoobarParams()


@dataclass
# A plugin that does not extend the parent Plugin class
class InvalidPlugin:
    name: str = "invalid_plugin"


@dataclass
class Config:
    plugin: Plugin = Plugin()


def test_overlapping_schemas(restore_singletons: Any) -> None:  # noqa: F811

    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
    cs.store(group="plugin", name="concrete", node=ConcretePlugin, path="plugin")

    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    cfg = config_loader.load_configuration(config_name="config", overrides=[])
    del cfg["hydra"]
    assert cfg == {"plugin": {"name": "???", "params": "???"}}
    assert cfg.plugin._type == Plugin

    cfg = config_loader.load_configuration(
        config_name="config", overrides=["plugin=concrete"]
    )
    del cfg["hydra"]
    assert cfg == {"plugin": {"name": "foobar_plugin", "params": {"foo": 10}}}
    assert cfg.plugin._type == ConcretePlugin
    assert cfg.plugin.params._type == ConcretePlugin.FoobarParams
    with pytest.raises(ValidationError):
        cfg.plugin = 10


def test_invalid_plugin_merge(restore_singletons: Any) -> Any:  # noqa: F811
    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
    cs.store(group="plugin", name="invalid", node=InvalidPlugin, path="plugin")

    cl = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    with pytest.raises(ValidationError):
        cl.load_configuration(config_name="config", overrides=["plugin=invalid"])
