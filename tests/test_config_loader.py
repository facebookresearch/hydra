# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from dataclasses import dataclass
from typing import Any, List

import pytest
from omegaconf import MISSING, OmegaConf, ValidationError, open_dict

from hydra._internal.config_loader_impl import (
    ConfigLoaderImpl,
    DefaultElement,
    ParsedConfigOverride,
    ParsedOverride,
)
from hydra._internal.utils import create_config_search_path
from hydra.core.config_loader import LoadTrace
from hydra.core.config_store import ConfigStore, ConfigStoreWithProvider
from hydra.core.utils import env_override
from hydra.errors import HydraException, MissingConfigException
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


@dataclass
class MySQLConfig:
    driver: str = MISSING
    host: str = MISSING
    port: int = MISSING
    user: str = MISSING
    password: str = MISSING


@dataclass
class TopLevelConfig:
    normal_yaml_config: bool = MISSING
    db: MySQLConfig = MySQLConfig()


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
                ["group1@:pkg2=option1"],
                {"pkg2": {"group1_option1": True}, "pkg1": {"group2_option1": True}},
                id="override_unspecified_pkg_of_default",
            ),
            pytest.param(
                ["group1@:pkg1=option1"],
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
                ["+group1@pkg3=option1"],
                {
                    "pkg1": {"group1_option1": True},
                    "pkg2": {"group1_option1": True},
                    "pkg3": {"group1_option1": True},
                },
                id="append",
            ),
            pytest.param(
                ["~group1@pkg1"],
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

    def test_load_adding_group_not_in_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml",
            overrides=["+group2=file1"],
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

    def test_load_config_with_schema(
        self, hydra_restore_singletons: Any, path: str
    ) -> None:

        ConfigStore.instance().store(
            name="config", node=TopLevelConfig, provider="this_test"
        )
        ConfigStore.instance().store(
            group="db", name="mysql", node=MySQLConfig, provider="this_test",
        )

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )

        cfg = config_loader.load_configuration(
            config_name="config", overrides=["+db=mysql"]
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {
            "normal_yaml_config": True,
            "db": {
                "driver": "mysql",
                "host": "???",
                "port": "???",
                "user": "omry",
                "password": "secret",
            },
        }

        expected = hydra_load_list.copy()
        expected.append(LoadTrace("config", path, "main", "this_test"))
        expected.append(LoadTrace("db/mysql", path, "main", "this_test"))
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
        self, hydra_restore_singletons: Any, path: str
    ) -> None:

        with ConfigStoreWithProvider("this_test") as cs:
            cs.store(name="config", node=TopLevelConfig)
            cs.store(group="db", name="mysql", node=MySQLConfig, package="db")

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config", overrides=["+db=mysql"], strict=False
        )

        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {
            "normal_yaml_config": True,
            "db": {
                "driver": "mysql",
                "host": "???",
                "port": "???",
                "user": "omry",
                "password": "secret",
            },
        }

        expected = hydra_load_list.copy()
        expected.append(LoadTrace("config", path, "main", "this_test"))
        expected.append(LoadTrace("db/mysql", path, "main", "this_test"))
        assert config_loader.get_load_history() == expected

    def test_assign_null(
        self, hydra_restore_singletons: Any, path: str, recwarn: Any
    ) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yaml", overrides=["abc=null"]
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"normal_yaml_config": True, "abc": None}
        assert len(recwarn) == 0


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
        ("config.yaml", ["~hydra/launcher"]),
        # remove from both
        ("removing-hydra-launcher-default.yaml", ["~hydra/launcher"]),
        # second overrides removes
        ("config.yaml", ["hydra/launcher=submitit", "~hydra/launcher"]),
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
            "examples/jupyter_notebooks/cloud_app/conf"
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


def test_load_schema_as_config(hydra_restore_singletons: Any) -> None:
    """
    Load structured config as a configuration
    """
    ConfigStore.instance().store(
        name="config", node=TopLevelConfig, provider="this_test"
    )

    ConfigStore.instance().store(
        name="db/mysql", node=MySQLConfig, provider="this_test",
    )

    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    cfg = config_loader.load_configuration(config_name="config", overrides=[])
    with open_dict(cfg):
        del cfg["hydra"]
    assert cfg == {
        "normal_yaml_config": "???",
        "db": {
            "driver": MISSING,
            "host": MISSING,
            "port": MISSING,
            "user": MISSING,
            "password": MISSING,
        },
    }

    expected = hydra_load_list.copy()
    expected.extend([LoadTrace("config", "structured://", "this_test", None)])
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


def test_overlapping_schemas(hydra_restore_singletons: Any) -> None:

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
        config_name="config", overrides=["+plugin=concrete"]
    )
    with open_dict(cfg):
        del cfg["hydra"]

    assert cfg == {"plugin": {"name": "foobar_plugin", "params": {"foo": 10}}}
    assert OmegaConf.get_type(cfg.plugin) == ConcretePlugin
    assert OmegaConf.get_type(cfg.plugin.params) == ConcretePlugin.FoobarParams
    with pytest.raises(ValidationError):
        cfg.plugin = 10


def test_invalid_plugin_merge(hydra_restore_singletons: Any) -> Any:
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
        # changing item
        pytest.param(
            "db=postgresql",
            ParsedOverride(None, "db", None, None, "postgresql"),
            id="change_option",
        ),
        pytest.param(
            "db@dest=postgresql",
            ParsedOverride(None, "db", "dest", None, "postgresql"),
            id="change_option",
        ),
        pytest.param(
            "db@src:dest=postgresql",
            ParsedOverride(None, "db", "src", "dest", "postgresql"),
            id="change_both",
        ),
        pytest.param(
            "db@dest",
            ParsedOverride(None, "db", "dest", None, None),
            id="change_package",
        ),
        pytest.param(
            "db@src:dest",
            ParsedOverride(None, "db", "src", "dest", None),
            id="change_package",
        ),
        # adding item
        pytest.param(
            "+model=resnet",
            ParsedOverride("+", "model", None, None, "resnet"),
            id="add_item",
        ),
        pytest.param(
            "+db@offsite_backup=mysql",
            ParsedOverride("+", "db", "offsite_backup", None, "mysql"),
            id="add_item",
        ),
        # deleting item
        pytest.param(
            "~db", ParsedOverride("~", "db", None, None, None), id="delete_item",
        ),
        pytest.param(
            "~db@src", ParsedOverride("~", "db", "src", None, None), id="delete_item",
        ),
        pytest.param(
            "~db", ParsedOverride("~", "db", None, None, None), id="delete_item",
        ),
        pytest.param(
            "~db@src", ParsedOverride("~", "db", "src", None, None), id="delete_item",
        ),
    ],
)
def test_parse_override(override: str, expected: ParsedOverride) -> None:
    ret = ConfigLoaderImpl._parse_override(override)
    assert ret.override == expected


config_parse_error_msg = (
    "Error parsing config override : '{override}'"
    "\nAccepted forms:"
    "\n\tOverride:  key=value"
    "\n\tAppend:   +key=value"
    "\n\tDelete:   ~key=value, ~key"
)


@pytest.mark.parametrize(  # type: ignore
    "override, expected",
    [
        pytest.param(
            "x.y.z=abc", ParsedConfigOverride(None, "x.y.z", "abc"), id="change_option",
        ),
        pytest.param(
            "+x.y.z=abc", ParsedConfigOverride("+", "x.y.z", "abc"), id="adding",
        ),
        pytest.param(
            "~x.y.z=abc", ParsedConfigOverride("~", "x.y.z", "abc"), id="adding",
        ),
        pytest.param("~x.y.z=", ParsedConfigOverride("~", "x.y.z", ""), id="adding"),
        pytest.param(
            "=a",
            pytest.raises(
                HydraException,
                match=re.escape(config_parse_error_msg.format(override="=a")),
            ),
            id="no_key",
        ),
    ],
)
def test_parse_config_override(override: str, expected: Any) -> None:
    if isinstance(expected, ParsedConfigOverride):
        ret = ConfigLoaderImpl._parse_config_override(override)
        assert ret == expected
    else:
        with expected:
            ConfigLoaderImpl._parse_config_override(override)


defaults_list = [{"db": "mysql"}, {"db@src": "mysql"}, {"hydra/launcher": "basic"}]


@pytest.mark.parametrize(  # type: ignore
    "input_defaults,overrides,expected",
    [
        # change item
        pytest.param(
            defaults_list,
            ["db=postgresql"],
            [{"db": "postgresql"}, {"db@src": "mysql"}, {"hydra/launcher": "basic"}],
            id="change_option",
        ),
        pytest.param(
            defaults_list,
            ["db@src=postgresql"],
            [{"db": "mysql"}, {"db@src": "postgresql"}, {"hydra/launcher": "basic"}],
            id="change_option",
        ),
        pytest.param(
            defaults_list,
            ["db@:dest=postgresql"],
            [
                {"db@dest": "postgresql"},
                {"db@src": "mysql"},
                {"hydra/launcher": "basic"},
            ],
            id="change_both",
        ),
        pytest.param(
            defaults_list,
            ["db@src:dest=postgresql"],
            [{"db": "mysql"}, {"db@dest": "postgresql"}, {"hydra/launcher": "basic"}],
            id="change_both",
        ),
        pytest.param(
            defaults_list,
            ["db@XXX:dest=postgresql"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not rename package. No match for 'db@XXX' in the defaults list."
                ),
            ),
            id="change_both_invalid_package",
        ),
        pytest.param(
            defaults_list,
            ["db@:dest"],
            [{"db@dest": "mysql"}, {"db@src": "mysql"}, {"hydra/launcher": "basic"}],
            id="change_package",
        ),
        pytest.param(
            defaults_list,
            ["db@src:dest"],
            [{"db": "mysql"}, {"db@dest": "mysql"}, {"hydra/launcher": "basic"}],
            id="change_package",
        ),
        pytest.param(
            defaults_list,
            ["db@XXX:dest"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not rename package. No match for 'db@XXX' in the defaults list."
                ),
            ),
            id="change_package_from_invalid",
        ),
        # adding item
        pytest.param([], ["+db=mysql"], [{"db": "mysql"}], id="adding_item"),
        pytest.param(
            defaults_list,
            ["+db@backup=mysql"],
            [
                {"db": "mysql"},
                {"db@src": "mysql"},
                {"hydra/launcher": "basic"},
                {"db@backup": "mysql"},
            ],
            id="adding_item_at_package",
        ),
        pytest.param(
            defaults_list,
            ["+db=mysql"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not add. An item matching 'db' is already in the defaults list"
                ),
            ),
            id="adding_duplicate_item",
        ),
        pytest.param(
            defaults_list,
            ["+db@src:foo=mysql"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Add syntax does not support package rename, remove + prefix"
                ),
            ),
            id="add_rename_error",
        ),
        pytest.param(
            defaults_list,
            ["+db@src=mysql"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not add. An item matching 'db@src' is already in the defaults list"
                ),
            ),
            id="adding_duplicate_item",
        ),
        pytest.param(
            [],
            ["db=mysql"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not override 'db'. No match in the defaults list."
                    "\nTo append to your default list use +db=mysql"
                ),
            ),
            id="adding_without_plus",
        ),
        # deleting item
        pytest.param(
            [],
            ["~db=mysql"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not delete. No match for 'db' in the defaults list."
                ),
            ),
            id="delete_no_match",
        ),
        pytest.param(
            defaults_list,
            ["~db"],
            [{"db@src": "mysql"}, {"hydra/launcher": "basic"}],
            id="delete",
        ),
        pytest.param(
            defaults_list,
            ["~db=mysql"],
            [{"db@src": "mysql"}, {"hydra/launcher": "basic"}],
            id="delete",
        ),
        pytest.param(
            defaults_list,
            ["~db=postgresql"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not delete. No match for 'db=postgresql' in the defaults list."
                ),
            ),
            id="delete_mismatch_value",
        ),
        pytest.param(
            defaults_list,
            ["~db@src"],
            [{"db": "mysql"}, {"hydra/launcher": "basic"}],
            id="delete",
        ),
        # syntax error
        pytest.param(
            defaults_list,
            ["db"],
            pytest.raises(
                HydraException,
                match=re.escape("Error parsing config group override : 'db'"),
            ),
            id="syntax_error",
        ),
    ],
)
def test_apply_overrides_to_defaults(
    input_defaults: List[str], overrides: List[str], expected: Any
) -> None:
    defaults = ConfigLoaderImpl._parse_defaults(
        OmegaConf.create({"defaults": input_defaults})
    )
    parsed_overrides = [
        ConfigLoaderImpl._parse_override(override) for override in overrides
    ]

    if isinstance(expected, list):
        expected_defaults = ConfigLoaderImpl._parse_defaults(
            OmegaConf.create({"defaults": expected})
        )
        ConfigLoaderImpl._apply_overrides_to_defaults(
            overrides=parsed_overrides, defaults=defaults
        )
        assert defaults == expected_defaults
    else:
        with expected:
            ConfigLoaderImpl._apply_overrides_to_defaults(
                overrides=parsed_overrides, defaults=defaults
            )


def test_delete_by_assigning_null_is_deprecated() -> None:
    msg = (
        "\nRemoving from the defaults list by assigning 'null' "
        "is deprecated and will be removed in Hydra 1.1."
        "\nUse ~db"
    )

    defaults = ConfigLoaderImpl._parse_defaults(
        OmegaConf.create({"defaults": [{"db": "mysql"}]})
    )
    parsed_overrides = [ConfigLoaderImpl._parse_override("db=null")]

    with pytest.warns(expected_warning=UserWarning, match=re.escape(msg)):
        assert parsed_overrides[0].override.is_delete()
        ConfigLoaderImpl._apply_overrides_to_defaults(
            overrides=parsed_overrides, defaults=defaults
        )
        assert defaults == []


@pytest.mark.parametrize(  # type: ignore
    "input_cfg,strict,overrides,expected",
    [
        # append
        pytest.param({}, False, ["x=10"], {"x": 10}, id="append"),
        pytest.param(
            {},
            True,
            ["x=10"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not override 'x'. No match in config."
                    "\nTo append to your config use +x=10"
                ),
            ),
            id="append",
        ),
        pytest.param({}, True, ["+x=10"], {"x": 10}, id="append"),
        # append item with @
        pytest.param(
            {},
            False,
            ["user@hostname=active"],
            {"user@hostname": "active"},
            id="append@",
        ),
        pytest.param(
            {},
            True,
            ["+user@hostname=active"],
            {"user@hostname": "active"},
            id="append@",
        ),
        pytest.param(
            {"x": 20},
            True,
            ["+x=10"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not append to config. An item is already at 'x'"
                ),
            ),
            id="append",
        ),
        # override
        pytest.param({"x": 20}, False, ["x=10"], {"x": 10}, id="override"),
        pytest.param({"x": 20}, True, ["x=10"], {"x": 10}, id="override"),
        pytest.param(
            {"x": 20}, False, ["x=null"], {"x": None}, id="override_with_null"
        ),
        # delete
        pytest.param({"x": 20}, False, ["~x"], {}, id="delete"),
        pytest.param({"x": 20}, False, ["~x=20"], {}, id="delete"),
        pytest.param({"x": {"y": 10}}, False, ["~x"], {}, id="delete"),
        pytest.param({"x": {"y": 10}}, False, ["~x.y"], {"x": {}}, id="delete"),
        pytest.param({"x": {"y": 10}}, False, ["~x.y=10"], {"x": {}}, id="delete"),
        pytest.param({"x": 20}, True, ["~x"], {}, id="delete_strict"),
        pytest.param({"x": 20}, True, ["~x=20"], {}, id="delete_strict"),
        pytest.param({"x": {"y": 10}}, True, ["~x"], {}, id="delete_strict"),
        pytest.param({"x": {"y": 10}}, True, ["~x.y"], {"x": {}}, id="delete_strict"),
        pytest.param(
            {"x": {"y": 10}}, True, ["~x.y=10"], {"x": {}}, id="delete_strict"
        ),
        pytest.param(
            {"x": 20},
            False,
            ["~z"],
            pytest.raises(
                HydraException,
                match=re.escape("Could not delete from config. 'z' does not exist."),
            ),
            id="delete_error_key",
        ),
        pytest.param(
            {"x": 20},
            False,
            ["~x=10"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not delete from config. The value of 'x' is 20 and not 10."
                ),
            ),
            id="delete_error_value",
        ),
    ],
)
def test_apply_overrides_to_config(
    input_cfg: Any, strict: bool, overrides: List[str], expected: Any
) -> None:
    cfg = OmegaConf.create(input_cfg)
    OmegaConf.set_struct(cfg, strict)
    if isinstance(expected, dict):
        ConfigLoaderImpl._apply_overrides_to_config(overrides=overrides, cfg=cfg)
        assert cfg == expected
    else:
        with expected:
            ConfigLoaderImpl._apply_overrides_to_config(overrides=overrides, cfg=cfg)
