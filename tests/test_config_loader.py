# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List

import pytest
from omegaconf import MISSING, OmegaConf, ValidationError, open_dict

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.utils import create_config_search_path
from hydra.core.config_loader import LoadTrace
from hydra.core.config_store import ConfigStore, ConfigStoreWithProvider
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.utils import env_override, setup_globals
from hydra.errors import (
    ConfigCompositionException,
    HydraException,
    MissingConfigException,
)
from hydra.test_utils.test_utils import chdir_hydra_root
from hydra.types import RunMode
from tests import UserGroup

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
    LoadTrace(
        config_group=None,
        config_name="hydra_config",
        search_path="structured://",
        provider="hydra",
    ),
    LoadTrace(
        config_group="hydra/hydra_logging",
        config_name="default",
        search_path="pkg://hydra.conf",
        provider="hydra",
        parent="hydra_config",
    ),
    LoadTrace(
        config_group="hydra/job_logging",
        config_name="default",
        search_path="pkg://hydra.conf",
        provider="hydra",
        parent="hydra_config",
    ),
    LoadTrace(
        config_group="hydra/launcher",
        config_name="basic",
        search_path="structured://",
        provider="hydra",
        parent="hydra_config",
    ),
    LoadTrace(
        config_group="hydra/sweeper",
        config_name="basic",
        search_path="structured://",
        provider="hydra",
        parent="hydra_config",
    ),
    LoadTrace(
        config_group="hydra/output",
        config_name="default",
        search_path="pkg://hydra.conf",
        provider="hydra",
        parent="hydra_config",
    ),
    LoadTrace(
        config_group="hydra/help",
        config_name="default",
        search_path="pkg://hydra.conf",
        provider="hydra",
        parent="hydra_config",
    ),
    LoadTrace(
        config_group="hydra/hydra_help",
        config_name="default",
        search_path="pkg://hydra.conf",
        provider="hydra",
        parent="hydra_config",
    ),
]


def assert_same_composition_trace(composition_trace: Any, expected: Any) -> None:
    actual = [LoadTrace(**x) for x in composition_trace]
    assert actual == expected


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
            config_name="config.yaml",
            strict=False,
            overrides=["abc=123"],
            run_mode=RunMode.RUN,
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
                config_name="missing-default.yaml",
                overrides=[],
                strict=False,
                run_mode=RunMode.RUN,
            )

    def test_load_with_missing_optional_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="missing-optional-default.yaml",
            overrides=[],
            strict=False,
            run_mode=RunMode.RUN,
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {}

    def test_load_with_optional_default(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default.yaml",
            overrides=[],
            strict=False,
            run_mode=RunMode.RUN,
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"foo": 10}

    @pytest.mark.parametrize(  # type: ignore
        "override,expected",
        [
            ("group1@:xyz=file2", {"xyz": {"foo": 20}}),
            ("group1@:a.b=file2", {"a": {"b": {"foo": 20}}}),
        ],
    )
    def test_load_changing_group_in_default(
        self, path: str, override: str, expected: Dict[Any, Any]
    ) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="optional-default",
            overrides=[override],
            strict=False,
            run_mode=RunMode.RUN,
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == expected

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
            config_name="pkg_override", overrides=overrides, run_mode=RunMode.RUN
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
            config_name="two_packages_one_group",
            overrides=overrides,
            run_mode=RunMode.RUN,
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
            run_mode=RunMode.RUN,
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
            run_mode=RunMode.RUN,
        )
        assert cfg.hydra.run.dir == "abc"

    def test_change_run_dir_with_config(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="overriding_run_dir.yaml",
            overrides=[],
            strict=False,
            run_mode=RunMode.RUN,
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
            config_name="compose.yaml",
            overrides=["foo=ZZZ"],
            strict=True,
            run_mode=RunMode.RUN,
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
                config_name="compose.yaml",
                overrides=["f00=ZZZ"],
                strict=True,
                run_mode=RunMode.RUN,
            )

    def test_load_history(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="missing-optional-default.yaml",
            overrides=[],
            run_mode=RunMode.RUN,
        )
        expected = deepcopy(hydra_load_list)
        expected.append(
            LoadTrace(
                config_group=None,
                config_name="missing-optional-default.yaml",
                provider="main",
                search_path=path,
            )
        )
        expected.append(
            LoadTrace(
                config_group="foo",
                config_name="missing",
                skip_reason="missing_optional_config",
                parent="missing-optional-default.yaml",
            )
        )

        assert_same_composition_trace(cfg.hydra.composition_trace, expected)

    def test_load_history_with_basic_launcher(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="custom_default_launcher.yaml",
            overrides=["hydra/launcher=basic"],
            strict=False,
            run_mode=RunMode.RUN,
        )

        expected = deepcopy(hydra_load_list)
        expected.append(
            LoadTrace(
                config_name="custom_default_launcher.yaml",
                search_path=path,
                provider="main",
            )
        )
        assert_same_composition_trace(cfg.hydra.composition_trace, expected)

    def test_load_yml_file(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yml", overrides=[], strict=False, run_mode=RunMode.RUN
        )
        with open_dict(cfg):
            del cfg["hydra"]

        assert cfg == {"yml_file_here": True}

    def test_override_with_equals(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yaml",
            overrides=["abc='cde=12'"],
            strict=False,
            run_mode=RunMode.RUN,
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == OmegaConf.create({"normal_yaml_config": True, "abc": "cde=12"})

    def test_compose_file_with_dot(self, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="compose.yaml",
            overrides=["group1=abc.cde"],
            strict=False,
            run_mode=RunMode.RUN,
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
            group="db", name="mysql", node=MySQLConfig, provider="this_test"
        )

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )

        cfg = config_loader.load_configuration(
            config_name="config", overrides=["+db=mysql"], run_mode=RunMode.RUN
        )

        expected = deepcopy(hydra_load_list)
        expected.append(
            LoadTrace(
                config_name="config",
                search_path=path,
                provider="main",
                schema_provider="this_test",
            )
        )
        expected.append(
            LoadTrace(
                config_group="db",
                config_name="mysql",
                search_path=path,
                provider="main",
                schema_provider="this_test",
                parent="overrides",
            )
        )
        assert_same_composition_trace(cfg.hydra.composition_trace, expected)

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

        # verify illegal modification is rejected at runtime
        with pytest.raises(ValidationError):
            cfg.db.port = "fail"

        # verify illegal override is rejected during load
        with pytest.raises(HydraException):
            config_loader.load_configuration(
                config_name="db/mysql", overrides=["db.port=fail"], run_mode=RunMode.RUN
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
            config_name="config",
            overrides=["+db=mysql"],
            strict=False,
            run_mode=RunMode.RUN,
        )

        expected = deepcopy(hydra_load_list)
        expected.append(
            LoadTrace(
                config_name="config",
                search_path=path,
                provider="main",
                schema_provider="this_test",
            )
        )
        expected.append(
            LoadTrace(
                config_group="db",
                config_name="mysql",
                search_path=path,
                provider="main",
                schema_provider="this_test",
                parent="overrides",
            )
        )
        assert_same_composition_trace(cfg.hydra.composition_trace, expected)

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

    def test_assign_null(self, hydra_restore_singletons: Any, path: str) -> None:
        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        cfg = config_loader.load_configuration(
            config_name="config.yaml", overrides=["+abc=null"], run_mode=RunMode.RUN
        )
        with open_dict(cfg):
            del cfg["hydra"]
        assert cfg == {"normal_yaml_config": True, "abc": None}

    def test_sweep_config_cache(
        self, hydra_restore_singletons: Any, path: str, monkeypatch: Any
    ) -> None:
        setup_globals()

        config_loader = ConfigLoaderImpl(
            config_search_path=create_config_search_path(path)
        )
        master_cfg = config_loader.load_configuration(
            config_name="config.yaml",
            strict=False,
            overrides=["+time=${now:%H-%M-%S}", "+home=${env:HOME}"],
            run_mode=RunMode.RUN,
        )

        # trigger resolution by type assertion
        assert type(master_cfg.time) == str
        assert type(master_cfg.home) == str

        master_cfg_cache = OmegaConf.get_cache(master_cfg)
        assert "now" in master_cfg_cache.keys() and "env" in master_cfg_cache.keys()
        assert master_cfg.home == os.environ["HOME"]

        sweep_cfg = config_loader.load_sweep_config(
            master_config=master_cfg,
            sweep_overrides=["+time=${now:%H-%M-%S}", "+home=${env:HOME}"],
        )

        sweep_cfg_cache = OmegaConf.get_cache(sweep_cfg)
        assert len(sweep_cfg_cache.keys()) == 1 and "now" in sweep_cfg_cache.keys()
        assert sweep_cfg_cache["now"] == master_cfg_cache["now"]
        monkeypatch.setenv("HOME", "/another/home/dir/")
        assert sweep_cfg.home == os.getenv("HOME")


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
    cfg = config_loader.load_configuration(
        config_name=config_file, overrides=overrides, strict=False, run_mode=RunMode.RUN
    )

    expected = deepcopy(hydra_load_list)
    for x in expected:
        if x.config_group == "hydra/launcher":
            x.skip_reason = "deleted_from_list"
            x.search_path = None
            x.provider = None
    expected.append(
        LoadTrace(
            config_name=config_file,
            search_path="file://hydra/test_utils/configs",
            provider="main",
        )
    )
    assert_same_composition_trace(cfg.hydra.composition_trace, expected)


def test_defaults_not_list_exception() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )
    with pytest.raises(ValueError):
        config_loader.load_configuration(
            config_name="defaults_not_list.yaml",
            overrides=[],
            strict=False,
            run_mode=RunMode.RUN,
        )


def test_override_hydra_config_value_from_config_file() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )

    cfg = config_loader.load_configuration(
        config_name="overriding_output_dir.yaml",
        overrides=[],
        strict=False,
        run_mode=RunMode.RUN,
    )
    assert cfg.hydra.run.dir == "foo"


def test_override_hydra_config_group_from_config_file() -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )

    cfg = config_loader.load_configuration(
        config_name="overriding_logging_default.yaml",
        overrides=[],
        strict=False,
        run_mode=RunMode.RUN,
    )
    expected = [
        LoadTrace(
            config_name="hydra_config", search_path="structured://", provider="hydra"
        ),
        LoadTrace(
            config_group="hydra/hydra_logging",
            config_name="hydra_debug",
            search_path="pkg://hydra.conf",
            provider="hydra",
            parent="hydra_config",
        ),
        LoadTrace(
            config_group="hydra/job_logging",
            config_name="disabled",
            search_path="pkg://hydra.conf",
            provider="hydra",
            parent="hydra_config",
        ),
        LoadTrace(
            config_group="hydra/launcher",
            config_name="basic",
            search_path=None,
            provider=None,
            parent="hydra_config",
            skip_reason="deleted_from_list",
        ),
        LoadTrace(
            config_group="hydra/sweeper",
            config_name="basic",
            search_path="structured://",
            provider="hydra",
            parent="hydra_config",
        ),
        LoadTrace(
            config_group="hydra/output",
            config_name="default",
            search_path="pkg://hydra.conf",
            provider="hydra",
            parent="hydra_config",
        ),
        LoadTrace(
            config_group="hydra/help",
            config_name="default",
            search_path="pkg://hydra.conf",
            provider="hydra",
            parent="hydra_config",
        ),
        LoadTrace(
            config_group="hydra/hydra_help",
            config_name="default",
            search_path="pkg://hydra.conf",
            provider="hydra",
            parent="hydra_config",
        ),
        LoadTrace(
            config_name="overriding_logging_default.yaml",
            search_path="file://hydra/test_utils/configs",
            provider="main",
        ),
    ]

    assert_same_composition_trace(cfg.hydra.composition_trace, expected)


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
    cfg = config_loader.load_configuration(
        config_name="non_config_group_default.yaml",
        overrides=[],
        strict=False,
        run_mode=RunMode.RUN,
    )

    expected = deepcopy(hydra_load_list)
    expected.extend(
        [
            LoadTrace(
                config_name="non_config_group_default.yaml",
                search_path="file://hydra/test_utils/configs",
                provider="main",
            ),
            LoadTrace(
                config_name="some_config",
                search_path="file://hydra/test_utils/configs",
                provider="main",
                parent="non_config_group_default.yaml",
            ),
        ]
    )

    assert_same_composition_trace(cfg.hydra.composition_trace, expected)


def test_mixed_composition_order() -> None:
    """
    Tests that the order of mixed composition (defaults contains both config group and non config group
    items) is correct
    """
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path("hydra/test_utils/configs")
    )
    cfg = config_loader.load_configuration(
        config_name="mixed_compose.yaml",
        overrides=[],
        strict=False,
        run_mode=RunMode.RUN,
    )

    expected = deepcopy(hydra_load_list)
    expected.extend(
        [
            LoadTrace(
                config_name="mixed_compose.yaml",
                search_path="file://hydra/test_utils/configs",
                provider="main",
            ),
            LoadTrace(
                config_name="some_config",
                search_path="file://hydra/test_utils/configs",
                provider="main",
                parent="mixed_compose.yaml",
            ),
            LoadTrace(
                config_group="group1",
                config_name="file1",
                search_path="file://hydra/test_utils/configs",
                provider="main",
                parent="mixed_compose.yaml",
            ),
            LoadTrace(
                config_name="config",
                search_path="file://hydra/test_utils/configs",
                provider="main",
                parent="mixed_compose.yaml",
            ),
        ]
    )

    assert_same_composition_trace(cfg.hydra.composition_trace, expected)


def test_load_schema_as_config(hydra_restore_singletons: Any) -> None:
    """
    Load structured config as a configuration
    """
    ConfigStore.instance().store(
        name="config", node=TopLevelConfig, provider="this_test"
    )

    ConfigStore.instance().store(
        name="db/mysql", node=MySQLConfig, provider="this_test"
    )

    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    cfg = config_loader.load_configuration(
        config_name="config", overrides=[], run_mode=RunMode.RUN
    )

    expected = deepcopy(hydra_load_list)
    expected.extend(
        [
            LoadTrace(
                config_name="config", search_path="structured://", provider="this_test"
            )
        ]
    )
    assert_same_composition_trace(cfg.hydra.composition_trace, expected)

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
    cfg = config_loader.load_configuration(
        config_name="config", overrides=[], run_mode=RunMode.RUN
    )
    with open_dict(cfg):
        del cfg["hydra"]

    assert cfg == {"plugin": {"name": "???", "params": "???"}}
    assert OmegaConf.get_type(cfg.plugin) == Plugin

    cfg = config_loader.load_configuration(
        config_name="config", overrides=["+plugin=concrete"], run_mode=RunMode.RUN
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
        cl.load_configuration(
            config_name="config", overrides=["plugin=invalid"], run_mode=RunMode.RUN
        )


def test_job_env_copy() -> None:
    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    with env_override({"zonk": "123456"}):
        cfg = config_loader.load_configuration(
            config_name=None,
            overrides=["hydra.job.env_copy=[zonk]"],
            run_mode=RunMode.RUN,
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

    cfg = config_loader.load_configuration(
        config_name="config", overrides=overrides, run_mode=RunMode.RUN
    )
    with open_dict(cfg):
        del cfg["hydra"]
    assert cfg == expected


@pytest.mark.parametrize(  # type: ignore
    "input_cfg,overrides,expected",
    [
        # append
        pytest.param(
            {},
            ["x=10"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not override 'x'.\nTo append to your config use +x=10"
                ),
            ),
            id="append:error:no_match",
        ),
        pytest.param({}, ["+x=10"], {"x": 10}, id="append"),
        pytest.param({}, ["+x=[1,2,3]"], {"x": [1, 2, 3]}, id="append:list"),
        pytest.param({}, ["+x={}"], {"x": {}}, id="append:dict:empty"),
        pytest.param({}, ["+x={a:1}"], {"x": {"a": 1}}, id="append:dict"),
        pytest.param({}, ["+x={a:1,b:2}"], {"x": {"a": 1, "b": 2}}, id="append:dict"),
        pytest.param(
            {}, ["+x={a:10,b:20}"], {"x": {"a": 10, "b": 20}}, id="append:dict"
        ),
        pytest.param(
            {"x": 20},
            ["+x=10"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not append to config. An item is already at 'x'"
                ),
            ),
            id="append:error:already_there",
        ),
        # override
        pytest.param({"x": 20}, ["x=10"], {"x": 10}, id="override"),
        pytest.param({"x": 20}, ["x=10"], {"x": 10}, id="override"),
        pytest.param({"x": None}, ["x=[1,2,3]"], {"x": [1, 2, 3]}, id="override:list"),
        pytest.param({"x": 20}, ["x=null"], {"x": None}, id="override_with_null"),
        pytest.param({"x": {"a": 10}}, ["x={a:20}"], {"x": {"a": 20}}, id="merge_dict"),
        pytest.param(
            {"x": {"a": 10, "b": None}},
            ["x={b:20}"],
            {"x": {"a": 10, "b": 20}},
            id="merge_dict",
        ),
        pytest.param(
            {"x": {"a": 10}},
            ["+x={b:20}"],
            {"x": {"a": 10, "b": 20}},
            id="merge_dict",
        ),
        pytest.param(
            UserGroup,
            ["name=agents", "users=[]"],
            {"name": "agents", "users": []},
            id="merge_list",
        ),
        pytest.param(
            UserGroup,
            ["name=agents", "users=[{}]"],
            {"name": "agents", "users": [{"name": MISSING, "age": MISSING}]},
            id="merge_list",
        ),
        pytest.param(
            UserGroup,
            ["name=agents", "users=[{name:bond,age:7}]"],
            {"name": "agents", "users": [{"name": "bond", "age": 7}]},
            id="merge_list",
        ),
        pytest.param(
            UserGroup,
            ["name=agents", "users=[{name:bond,age:nope}]"],
            pytest.raises(
                ConfigCompositionException,
                match=re.escape("Error merging override users=[{name:bond,age:nope}]"),
            ),
            id="merge_list",
        ),
        # delete
        pytest.param({"x": 20}, ["~x"], {}, id="delete"),
        pytest.param({"x": 20}, ["~x=20"], {}, id="delete_strict"),
        pytest.param({"x": {"y": 10}}, ["~x"], {}, id="delete"),
        pytest.param({"x": {"y": 10}}, ["~x.y"], {"x": {}}, id="delete"),
        pytest.param({"x": {"y": 10}}, ["~x.y=10"], {"x": {}}, id="delete_strict"),
        pytest.param({"x": 20}, ["~x"], {}, id="delete"),
        pytest.param({"x": 20}, ["~x=20"], {}, id="delete_strict"),
        pytest.param({"x": {"y": 10}}, ["~x"], {}, id="delete"),
        pytest.param({"x": {"y": 10}}, ["~x.y"], {"x": {}}, id="delete"),
        pytest.param({"x": {"y": 10}}, ["~x.y=10"], {"x": {}}, id="delete_strict"),
        pytest.param({"x": [1, 2, 3]}, ["~x"], {}, id="delete:list"),
        pytest.param({"x": [1, 2, 3]}, ["~x=[1,2,3]"], {}, id="delete:list"),
        pytest.param(
            {"x": 20},
            ["~z"],
            pytest.raises(
                HydraException,
                match=re.escape("Could not delete from config. 'z' does not exist."),
            ),
            id="delete_error_key",
        ),
        pytest.param(
            {"x": 20},
            ["~x=10"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Could not delete from config. The value of 'x' is 20 and not 10."
                ),
            ),
            id="delete_error_value",
        ),
        pytest.param(
            {"x": 20},
            ["foo@bar=10"],
            pytest.raises(
                HydraException,
                match=re.escape(
                    "Override foo@bar=10 looks like a config group override, but config group 'foo' does not exist."
                ),
            ),
            id="config_group_missing",
        ),
    ],
)
def test_apply_overrides_to_config(
    input_cfg: Any, overrides: List[str], expected: Any
) -> None:
    cfg = OmegaConf.create(input_cfg)
    OmegaConf.set_struct(cfg, True)
    parser = OverridesParser.create()
    parsed = parser.parse_overrides(overrides=overrides)

    if isinstance(expected, dict):
        ConfigLoaderImpl._apply_overrides_to_config(overrides=parsed, cfg=cfg)
        assert cfg == expected
    else:
        with expected:
            ConfigLoaderImpl._apply_overrides_to_config(overrides=parsed, cfg=cfg)


@pytest.mark.parametrize(  # type: ignore
    "config,overrides,expected",
    [
        pytest.param(
            "config",
            [],
            {"optimizer": {"type": "nesterov", "lr": 0.001}},
            id="default_choice",
        ),
        pytest.param(
            "config",
            ["optimizer=adam"],
            {"optimizer": {"type": "adam", "lr": 0.1, "beta": 0.01}},
            id="default_change",
        ),
        pytest.param(
            # need to unset optimizer config group first, otherwise they get merged
            "config",
            ["optimizer={type:nesterov2,lr:1}"],
            {"optimizer": {"type": "nesterov2", "lr": 1}},
            id="dict_merge",
        ),
        pytest.param(
            # need to unset optimizer config group first, otherwise they get merged
            "config",
            ["+optimizer={foo:10}"],
            {"optimizer": {"type": "nesterov", "lr": 0.001, "foo": 10}},
            id="dict_merge_append",
        ),
        pytest.param(
            # need to unset optimizer config group first, otherwise they get merged
            "missing_default",
            ["~optimizer", "+optimizer={type:super,good:true,fast:true}"],
            {"optimizer": {"type": "super", "good": True, "fast": True}},
            id="dict_replace_default",
        ),
    ],
)
def test_overriding_with_dict(config: str, overrides: Any, expected: Any) -> None:
    config_loader = ConfigLoaderImpl(
        config_search_path=create_config_search_path(
            "tests/test_apps/app_with_cfg_groups/conf"
        ),
    )

    cfg = config_loader.load_configuration(
        config_name=config, overrides=overrides, run_mode=RunMode.RUN
    )
    with open_dict(cfg):
        del cfg["hydra"]
    assert cfg == expected
