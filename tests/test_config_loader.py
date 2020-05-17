# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any, List

import pkg_resources
import pytest
from omegaconf import MISSING, OmegaConf, ValidationError, open_dict

from hydra._internal.config_loader_impl import (
    ConfigLoaderImpl,
    DefaultElement,
    ParsedOverride,
)
from hydra._internal.utils import create_config_search_path
from hydra.core.config_loader import LoadTrace
from hydra.core.config_store import ConfigStore, ConfigStoreWithProvider
from hydra.core.errors import HydraException
from hydra.core.utils import env_override
from hydra.errors import MissingConfigException
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


@dataclass
class MySQLConfig:
    driver: str = MISSING
    host: str = MISSING
    port: int = MISSING
    user: str = MISSING
    password: str = MISSING


hydra_load_list: List[LoadTrace] = [
    LoadTrace("hydra_config", "structured://", "hydra", None),
    LoadTrace("hydra/hydra_logging/default", "pkg://hydra.conf", "hydra", None),
    LoadTrace("hydra/job_logging/default", "pkg://hydra.conf", "hydra", None),
    LoadTrace("hydra/launcher/basic", "pkg://hydra.conf", "hydra", None),
    LoadTrace("hydra/sweeper/basic", "pkg://hydra.conf", "hydra", "hydra"),
    LoadTrace("hydra/output/default", "pkg://hydra.conf", "hydra", None),
    LoadTrace("hydra/help/default", "pkg://hydra.conf", "hydra", None),
    LoadTrace("hydra/hydra_help/default", "pkg://hydra.conf", "hydra", None),
]


@pytest.mark.parametrize(
    "path",
    [
        pytest.param("file://hydra/test_utils/configs", id="file"),
        pytest.param("pkg://hydra.test_utils.configs", id="pkg"),
    ],
)
class TestConfigLoader:
    def test_load_configuration(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yaml", strict=False, overrides=["abc=123"]
        )
        with open_dict(cfg):
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
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {}

    def test_load_with_optional_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml", overrides=[], strict=False
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"foo": 10}

    def test_load_changing_group_in_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml",
            overrides=["group1=file2"],
            strict=False,
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"foo": 20}

    @pytest.mark.parametrize(  # type: ignore
        "overrides,expected",
        [
            pytest.param(
                [],
                {"group1_option1": True, "pkg1": {"group2_option1": True}},
                id="no_overrides",
            ),
            pytest.param(
                ["group1@pkg2=option1"],
                {"pkg2": {"group1_option1": True}, "pkg1": {"group2_option1": True}},
                id="override_unspecified_pkg_of_default",
            ),
            pytest.param(
                ["group1@pkg1=option1"],
                {"pkg1": {"group1_option1": True, "group2_option1": True}},
                id="override_two_groups_to_same_package",
            ),
        ],
    )
    def test_load_changing_group_and_package_in_default(
        self, path: str, overrides: List[str], expected: Any
    ) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(f"{path}/package_tests")
        )
        cfg = config_loader.load_configuration(
            config_name="pkg_override", overrides=overrides
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == expected

    @pytest.mark.parametrize(  # type: ignore
        "overrides,expected",
        [
            pytest.param(
                [],
                {"pkg1": {"group1_option1": True}, "pkg2": {"group1_option1": True}},
                id="baseline",
            ),
            pytest.param(
                ["group1@pkg3=option1"],
                {
                    "pkg1": {"group1_option1": True},
                    "pkg2": {"group1_option1": True},
                    "pkg3": {"group1_option1": True},
                },
                id="append",
            ),
            pytest.param(
                ["group1@pkg1=null"],
                {"pkg2": {"group1_option1": True}},
                id="delete_package",
            ),
            pytest.param(
                ["group1@pkg1:new_pkg=option1"],
                {"new_pkg": {"group1_option1": True}, "pkg2": {"group1_option1": True}},
                id="change_pkg1",
            ),
            pytest.param(
                ["group1@pkg2:new_pkg=option1"],
                {"pkg1": {"group1_option1": True}, "new_pkg": {"group1_option1": True}},
                id="change_pkg2",
            ),
        ],
    )
    def test_override_compose_two_package_one_group(
        self, path: str, overrides: List[str], expected: Any
    ) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(f"{path}/package_tests")
        )
        cfg = config_loader.load_configuration(
            config_name="two_packages_one_group", overrides=overrides
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == expected

    # TODO: Imlement and test: https://docs.google.com/document/d/1I--p8JpIWQujVZuyaM2J910ew9wJ01S0E3ye6uJnTmY/edit#
    # TODO: Primary config file default package will be _global_ for Hydra 1.0 and in the future.
    # TODO: Error if source package is not found: python two_packages.py db@MISSING:source1=mysql
    # TODO: should config_path in @hydra.main be search_path
    # TODO : test packages with nn-config group items
    # TODO: python tutorials/basic/4_defaults/my_app.py  db=312312 should be an error, not an exception.
    # TODO: Add tests for new tutorial examples (2.1.using_config, 2.2_strict mode)
    # TODO: split page 2 into 2.1_using_config and 2.2_strict_mode

    def test_load_adding_group_not_in_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml",
            overrides=["group2=file1"],
            strict=False,
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"foo": 10, "bar": 100}

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
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"foo": "ZZZ", "bar": 100}

        # Test that accessing a key that is not there will fail
        with pytest.raises(AttributeError):
            # noinspection PyStatementEffect
            cfg.not_here

        # Test that bad overrides triggers the KeyError
        with pytest.raises(HydraException):
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
        expected.append(LoadTrace("missing-optional-default.yaml", path, "main", None))
        expected.append(LoadTrace("foo/missing", None, None, None))

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
        expected.append(LoadTrace("custom_default_launcher.yaml", path, "main", None))
        assert config_loader.get_load_history() == expected

    def test_load_yml_file(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yml", overrides=[], strict=False
        )
        with open_dict(cfg):
            del cfg["hydra"]

        assert cfg == {"yml_file_here": True}

    def test_override_with_equals(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yaml", overrides=["abc='cde=12'"], strict=False
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == OmegaConf.create({"normal_yaml_config": True, "abc": "cde=12"})

    def test_compose_file_with_dot(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="compose.yaml", overrides=["group1=abc.cde"], strict=False
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"abc=cde": None, "bar": 100}

    def test_load_config_with_schema(self, restore_singletons: Any, path: str) -> None:

        ConfigStore.instance().store(
            group="db", name="mysql", node=MySQLConfig, provider="test_provider",
        )

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )

        cfg = config_loader.load_configuration(config_name="db/mysql", overrides=[])
        with open_dict(cfg):
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
        expected.append(LoadTrace("db/mysql", path, "main", "test_provider"))
        assert config_loader.get_load_history() == expected

        # verify illegal modification is rejected at runtime
        with pytest.raises(ValidationError):
            cfg.db.port = "fail"

        # verify illegal override is rejected during load
        with pytest.raises(HydraException):
            config_loader.load_configuration(
                config_name="db/mysql", overrides=["db.port=fail"]
            )

    def test_load_config_file_with_schema_validation(
        self, restore_singletons: Any, path: str
    ) -> None:

        with ConfigStoreWithProvider("test_provider") as config_store:
            config_store.store(group="db", name="mysql", node=MySQLConfig, package="db")

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="db/mysql", overrides=[], strict=False
        )

        with open_dict(cfg):
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
        expected.append(LoadTrace("db/mysql", path, "main", "test_provider"))
        assert config_loader.get_load_history() == expected


@pytest.mark.parametrize(  # type:ignore
    "in_primary,in_merged,expected",
    [
        ([], [], []),
        (
            [DefaultElement(config_group="a", config_name="aa")],
            [],
            [DefaultElement(config_group="a", config_name="aa")],
        ),
        (
            [DefaultElement(config_group="a", config_name="aa")],
            [DefaultElement(config_group="b", config_name="bb")],
            [
                DefaultElement(config_group="a", config_name="aa"),
                DefaultElement(config_group="b", config_name="bb"),
            ],
        ),
        (
            [
                DefaultElement(config_group="hydra_logging", config_name="default"),
                DefaultElement(config_group="job_logging", config_name="default"),
                DefaultElement(config_group="launcher", config_name="basic"),
                DefaultElement(config_group="sweeper", config_name="basic"),
            ],
            [
                DefaultElement(config_group="optimizer", config_name="nesterov"),
                DefaultElement(config_group="launcher", config_name="basic"),
            ],
            [
                DefaultElement(config_group="hydra_logging", config_name="default"),
                DefaultElement(config_group="job_logging", config_name="default"),
                DefaultElement(config_group="launcher", config_name="basic"),
                DefaultElement(config_group="sweeper", config_name="basic"),
                DefaultElement(config_group="optimizer", config_name="nesterov"),
            ],
        ),
    ],
)
def test_merge_default_lists(
    in_primary: List[DefaultElement],
    in_merged: List[DefaultElement],
    expected: List[DefaultElement],
) -> None:
    ConfigLoaderImpl._combine_default_lists(in_primary, in_merged)
    assert in_primary == expected


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
        filter(lambda x: x.filename != "hydra/launcher/basic", hydra_load_list.copy())
    )
    expected.append(
        LoadTrace(config_file, "file://hydra/test_utils/configs", "main", None)
    )
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
        LoadTrace("hydra_config", "structured://", "hydra", None),
        LoadTrace("hydra/hydra_logging/hydra_debug", "pkg://hydra.conf", "hydra", None),
        LoadTrace("hydra/job_logging/disabled", "pkg://hydra.conf", "hydra", None),
        LoadTrace("hydra/sweeper/basic", "pkg://hydra.conf", "hydra", "hydra"),
        LoadTrace("hydra/output/default", "pkg://hydra.conf", "hydra", None),
        LoadTrace("hydra/help/default", "pkg://hydra.conf", "hydra", None),
        LoadTrace("hydra/hydra_help/default", "pkg://hydra.conf", "hydra", None),
        LoadTrace(
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
            LoadTrace(
                "non_config_group_default.yaml",
                "file://hydra/test_utils/configs",
                "main",
                None,
            ),
            LoadTrace("some_config", "file://hydra/test_utils/configs", "main", None),
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
            LoadTrace(
                "mixed_compose.yaml", "file://hydra/test_utils/configs", "main", None
            ),
            LoadTrace("some_config", "file://hydra/test_utils/configs", "main", None),
            LoadTrace("group1/file1", "file://hydra/test_utils/configs", "main", None),
            LoadTrace("config", "file://hydra/test_utils/configs", "main", None),
        ]
    )

    assert config_loader.get_load_history() == expected


def test_load_schema_as_config(restore_singletons: Any) -> None:
    """
    Load structured config as a configuration
    """
    ConfigStore.instance().store(
        group="db", name="mysql", node=MySQLConfig, provider="test_provider",
    )

    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    cfg = config_loader.load_configuration(config_name="db/mysql", overrides=[])
    with open_dict(cfg):
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
    expected.extend([LoadTrace("db/mysql", "structured://", "test_provider", None)])
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


def test_overlapping_schemas(restore_singletons: Any) -> None:

    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
    cs.store(group="plugin", name="concrete", node=ConcretePlugin)

    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    cfg = config_loader.load_configuration(config_name="config", overrides=[])
    with open_dict(cfg):
        del cfg["hydra"]

    assert cfg == {"plugin": {"name": "???", "params": "???"}}
    assert OmegaConf.get_type(cfg.plugin) == Plugin

    cfg = config_loader.load_configuration(
        config_name="config", overrides=["plugin=concrete"]
    )
    with open_dict(cfg):
        del cfg["hydra"]

    assert cfg == {"plugin": {"name": "foobar_plugin", "params": {"foo": 10}}}
    assert OmegaConf.get_type(cfg.plugin) == ConcretePlugin
    assert OmegaConf.get_type(cfg.plugin.params) == ConcretePlugin.FoobarParams
    with pytest.raises(ValidationError):
        cfg.plugin = 10


def test_invalid_plugin_merge(restore_singletons: Any) -> Any:
    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
    cs.store(group="plugin", name="invalid", node=InvalidPlugin)

    cl = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    with pytest.raises(HydraException):
        cl.load_configuration(config_name="config", overrides=["plugin=invalid"])


def test_job_env_copy() -> None:
    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    with env_override({"zonk": "123456"}):
        cfg = config_loader.load_configuration(
            config_name=None, overrides=["hydra.job.env_copy=[zonk]"]
        )
        assert cfg.hydra.job.env_set == {"zonk": "123456"}


@pytest.mark.parametrize(  # type: ignore
    "overrides,expected",
    [
        (
            [],
            {
                "optimizer": {"type": "adam", "lr": 0.1, "beta": 0.01},
                "dataset": {"name": "imagenet", "path": "/datasets/imagenet"},
                "adam_imagenet": True,
            },
        ),
        (
            ["optimizer=nesterov"],
            {
                "optimizer": {"type": "nesterov", "lr": 0.001},
                "dataset": {"name": "imagenet", "path": "/datasets/imagenet"},
                "nesterov_imagenet": True,
            },
        ),
    ],
)
def test_complex_defaults(overrides: Any, expected: Any) -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path(
            "tests/test_apps/sweep_complex_defaults/conf"
        )
    )

    cfg = config_loader.load_configuration(config_name="config", overrides=overrides)
    with open_dict(cfg):
        del cfg["hydra"]
    assert cfg == expected


@pytest.mark.parametrize(  # type: ignore
    "override, expected",
    [
        ("key=value", ParsedOverride("key", None, None, "value")),
        ("key@pkg=value", ParsedOverride("key", "pkg", None, "value")),
        ("key@pkg1:pkg2=value", ParsedOverride("key", "pkg1", "pkg2", "value")),
        ("key@a.b.c:x.y.z=value", ParsedOverride("key", "a.b.c", "x.y.z", "value")),
        ("key@:pkg2=value", ParsedOverride("key", "", "pkg2", "value")),
        ("key@pkg1:=value", ParsedOverride("key", "pkg1", "", "value")),
        ("key=null", ParsedOverride("key", None, None, "null")),
        ("foo/bar=zoo", ParsedOverride("foo/bar", None, None, "zoo")),
    ],
)
def test_parse_override(override: str, expected: ParsedOverride) -> None:
    ret = ConfigLoaderImpl._parse_override(override)
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "overrides, expected",
    [
        # interpreted as a dotlist
        (["user@hostname=active"], {"user@hostname": "active"}),
        (["user@hostname.com=active"], {"user@hostname": {"com": "active"}}),
    ],
)
def test_override_config_key_with_at_symbol(
    overrides: List[str], expected: Any
) -> None:
    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    cfg = config_loader.load_configuration(config_name=None, overrides=overrides)
    with open_dict(cfg):
        del cfg["hydra"]
    assert cfg == expected
