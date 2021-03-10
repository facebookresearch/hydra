# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from omegaconf import OmegaConf
from pytest import fixture, mark, param, raises

from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.config_search_path import SearchPathQuery
from hydra.core.config_store import ConfigStore
from hydra.core.global_hydra import GlobalHydra
from hydra.errors import ConfigCompositionException, HydraException
from hydra.experimental import (
    compose,
    initialize,
    initialize_config_dir,
    initialize_config_module,
)
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


@fixture
def initialize_hydra(config_path: Optional[str]) -> Any:
    try:
        init = initialize(config_path=config_path)
        init.__enter__()
        yield
    finally:
        init.__exit__(*sys.exc_info())


@fixture
def initialize_hydra_no_path() -> Any:
    try:
        init = initialize()
        init.__enter__()
        yield
    finally:
        init.__exit__(*sys.exc_info())


def test_initialize(hydra_restore_singletons: Any) -> None:
    assert not GlobalHydra().is_initialized()
    initialize(config_path=None)
    assert GlobalHydra().is_initialized()


def test_initialize_with_config_path(hydra_restore_singletons: Any) -> None:
    assert not GlobalHydra().is_initialized()
    initialize(config_path="../hydra/test_utils/configs")
    assert GlobalHydra().is_initialized()

    gh = GlobalHydra.instance()
    assert gh.hydra is not None
    config_search_path = gh.hydra.config_loader.get_search_path()
    assert isinstance(config_search_path, ConfigSearchPathImpl)
    idx = config_search_path.find_first_match(
        SearchPathQuery(provider="main", path=None)
    )
    assert idx != -1


@mark.usefixtures("initialize_hydra")
@mark.parametrize("config_path", ["../hydra/test_utils/configs"])
@mark.parametrize(
    "config_file, overrides, expected",
    [
        (None, [], {}),
        (None, ["+foo=bar"], {"foo": "bar"}),
        ("compose", [], {"foo": 10, "bar": 100}),
        ("compose", ["group1=file2"], {"foo": 20, "bar": 100}),
    ],
)
class TestCompose:
    def test_compose_config(
        self,
        config_file: str,
        overrides: List[str],
        expected: Any,
    ) -> None:
        cfg = compose(config_file, overrides)
        assert cfg == expected

    def test_strict_failure_global_strict(
        self, config_file: str, overrides: List[str], expected: Any
    ) -> None:
        # default strict True, call is unspecified
        overrides.append("fooooooooo=bar")
        with raises(HydraException):
            compose(config_file, overrides)


@mark.usefixtures("hydra_restore_singletons")
@mark.parametrize(
    "config_file, overrides, expected",
    [
        # empty
        (None, [], {}),
        (
            None,
            ["+db=sqlite"],
            {
                "db": {
                    "driver": "sqlite",
                    "user": "???",
                    "pass": "???",
                    "file": "test.db",
                }
            },
        ),
        (
            None,
            ["+db=mysql", "+environment=production"],
            {"db": {"driver": "mysql", "user": "mysql", "pass": "r4Zn*jQ9JB1Rz2kfz"}},
        ),
        (
            None,
            ["+db=mysql", "+environment=production", "+application=donkey"],
            {
                "db": {"driver": "mysql", "user": "mysql", "pass": "r4Zn*jQ9JB1Rz2kfz"},
                "donkey": {"name": "kong", "rank": "king"},
            },
        ),
        (
            None,
            [
                "+db=mysql",
                "+environment=production",
                "+application=donkey",
                "donkey.name=Dapple",
                "donkey.rank=squire_donkey",
            ],
            {
                "db": {"driver": "mysql", "user": "mysql", "pass": "r4Zn*jQ9JB1Rz2kfz"},
                "donkey": {"name": "Dapple", "rank": "squire_donkey"},
            },
        ),
        # load config
        (
            "config",
            [],
            {
                "db": {
                    "driver": "sqlite",
                    "user": "test",
                    "pass": "test",
                    "file": "test.db",
                },
                "cloud": {"name": "local", "host": "localhost", "port": 9876},
            },
        ),
        (
            "config",
            ["environment=production", "db=mysql"],
            {
                "db": {"driver": "mysql", "user": "mysql", "pass": "r4Zn*jQ9JB1Rz2kfz"},
                "cloud": {"name": "local", "host": "localhost", "port": 9876},
            },
        ),
    ],
)
class TestComposeInits:
    def test_initialize_ctx(
        self, config_file: str, overrides: List[str], expected: Any
    ) -> None:
        with initialize(config_path="../examples/jupyter_notebooks/cloud_app/conf"):
            ret = compose(config_file, overrides)
            assert ret == expected

    def test_initialize_config_dir_ctx_with_relative_dir(
        self, config_file: str, overrides: List[str], expected: Any
    ) -> None:
        with raises(
            HydraException,
            match=re.escape(
                "initialize_config_dir() requires an absolute config_dir as input"
            ),
        ):
            with initialize_config_dir(
                config_dir="../examples/jupyter_notebooks/cloud_app/conf",
                job_name="job_name",
            ):
                ret = compose(config_file, overrides)
                assert ret == expected

    def test_initialize_config_module_ctx(
        self, config_file: str, overrides: List[str], expected: Any
    ) -> None:
        with initialize_config_module(
            config_module="examples.jupyter_notebooks.cloud_app.conf",
            job_name="job_name",
        ):
            ret = compose(config_file, overrides)
            assert ret == expected


def test_initialize_ctx_with_absolute_dir(
    hydra_restore_singletons: Any, tmpdir: Any
) -> None:
    with raises(
        HydraException, match=re.escape("config_path in initialize() must be relative")
    ):
        with initialize(config_path=str(tmpdir)):
            compose(overrides=["+test_group=test"])


def test_initialize_config_dir_ctx_with_absolute_dir(
    hydra_restore_singletons: Any, tmpdir: Any
) -> None:
    tmpdir = Path(tmpdir)
    (tmpdir / "test_group").mkdir(parents=True)
    cfg = OmegaConf.create({"foo": "bar"})

    cfg_file = tmpdir / "test_group" / "test.yaml"
    with open(str(cfg_file), "w") as f:
        OmegaConf.save(cfg, f)

    with initialize_config_dir(config_dir=str(tmpdir)):
        ret = compose(overrides=["+test_group=test"])
        assert ret == {"test_group": cfg}


@mark.parametrize(
    "job_name,expected", [(None, "test_compose"), ("test_job", "test_job")]
)
def test_jobname_override_initialize_ctx(
    hydra_restore_singletons: Any, job_name: Optional[str], expected: str
) -> None:
    with initialize(
        config_path="../examples/jupyter_notebooks/cloud_app/conf", job_name=job_name
    ):
        ret = compose(return_hydra_config=True)
        assert ret.hydra.job.name == expected


def test_jobname_override_initialize_config_dir_ctx(
    hydra_restore_singletons: Any, tmpdir: Any
) -> None:
    with initialize_config_dir(config_dir=str(tmpdir), job_name="test_job"):
        ret = compose(return_hydra_config=True)
        assert ret.hydra.job.name == "test_job"


def test_initialize_config_module_ctx(hydra_restore_singletons: Any) -> None:
    with initialize_config_module(
        config_module="examples.jupyter_notebooks.cloud_app.conf"
    ):
        ret = compose(return_hydra_config=True)
        assert ret.hydra.job.name == "app"

    with initialize_config_module(
        config_module="examples.jupyter_notebooks.cloud_app.conf", job_name="test_job"
    ):
        ret = compose(return_hydra_config=True)
        assert ret.hydra.job.name == "test_job"

    with initialize_config_module(
        config_module="examples.jupyter_notebooks.cloud_app.conf", job_name="test_job"
    ):
        ret = compose(return_hydra_config=True)
        assert ret.hydra.job.name == "test_job"


def test_missing_init_py_error(hydra_restore_singletons: Any) -> None:
    expected = (
        "Primary config module 'hydra.test_utils.configs.missing_init_py' not found."
        "\nCheck that it's correct and contains an __init__.py file"
    )

    with raises(Exception, match=re.escape(expected)):
        with initialize_config_module(
            config_module="hydra.test_utils.configs.missing_init_py"
        ):
            hydra = GlobalHydra.instance().hydra
            assert hydra is not None
            compose(config_name="test.yaml", overrides=[])


def test_missing_bad_config_dir_error(hydra_restore_singletons: Any) -> None:
    expected = (
        "Primary config directory not found."
        "\nCheck that the config directory '/no_way_in_hell_1234567890' exists and readable"
    )

    with raises(Exception, match=re.escape(expected)):
        with initialize_config_dir(config_dir="/no_way_in_hell_1234567890"):
            hydra = GlobalHydra.instance().hydra
            assert hydra is not None
            compose(config_name="test.yaml", overrides=[])


def test_initialize_with_module(hydra_restore_singletons: Any) -> None:
    with initialize_config_module(
        config_module="tests.test_apps.app_with_cfg_groups.conf", job_name="my_pp"
    ):
        assert compose(config_name="config") == {
            "optimizer": {"type": "nesterov", "lr": 0.001}
        }


def test_hydra_main_passthrough(hydra_restore_singletons: Any) -> None:
    with initialize(config_path="test_apps/app_with_cfg_groups/conf"):
        from tests.test_apps.app_with_cfg_groups.my_app import my_app  # type: ignore

        cfg = compose(config_name="config", overrides=["optimizer.lr=1.0"])
        assert my_app(cfg) == {"optimizer": {"type": "nesterov", "lr": 1.0}}


def test_initialization_root_module(monkeypatch: Any) -> None:
    monkeypatch.chdir("tests/test_apps/init_in_app_without_module")
    subprocess.check_call([sys.executable, "main.py"])
    subprocess.check_call([sys.executable, "-m", "main"])


@mark.usefixtures("initialize_hydra_no_path")
@mark.parametrize(
    ("overrides", "expected"),
    [
        param(["+map.foo=bar"], {"map": {"foo": "bar"}}, id="add_with_plus"),
        param(["map.foo=bar"], raises(ConfigCompositionException), id="add_no_plus"),
    ],
)
def test_adding_to_sc_dict(
    hydra_restore_singletons: Any, overrides: List[str], expected: Any
) -> None:
    @dataclass
    class Config:
        map: Dict[str, str] = field(default_factory=dict)

    ConfigStore.instance().store(name="config", node=Config)

    if isinstance(expected, dict):
        cfg = compose(config_name="config", overrides=overrides)
        assert cfg == expected
    else:
        with expected:
            compose(config_name="config", overrides=overrides)


@mark.parametrize("override", ["hydra.foo=bar", "hydra.job_logging.foo=bar"])
def test_hydra_node_validated(initialize_hydra_no_path: Any, override: str) -> None:
    with raises(ConfigCompositionException):
        compose(overrides=[override])


@mark.usefixtures("hydra_restore_singletons")
@mark.usefixtures("initialize_hydra_no_path")
class TestAdd:
    def test_add(self) -> None:
        ConfigStore.instance().store(name="config", node={"key": 0})
        with raises(
            ConfigCompositionException,
            match="Could not append to config. An item is already at 'key'",
        ):
            compose(config_name="config", overrides=["+key=value"])

        cfg = compose(config_name="config", overrides=["key=1"])
        assert cfg == {"key": 1}

    def test_force_add(self) -> None:
        ConfigStore.instance().store(name="config", node={"key": 0})
        cfg = compose(config_name="config", overrides=["++key=1"])
        assert cfg == {"key": 1}

        cfg = compose(config_name="config", overrides=["++key2=1"])
        assert cfg == {"key": 0, "key2": 1}

    def test_add_config_group(self) -> None:
        ConfigStore.instance().store(group="group", name="a0", node={"key": 0})
        ConfigStore.instance().store(group="group", name="a1", node={"key": 1})
        # overriding non existing group throws
        with raises(ConfigCompositionException):
            compose(overrides=["group=a0"])

        # appending a new group
        cfg = compose(overrides=["+group=a0"])
        assert cfg == {"group": {"key": 0}}

        # force adding is not supported for config groups.
        with raises(
            ConfigCompositionException,
            match=re.escape(
                "force-add of config groups is not supported: '++group=a1'"
            ),
        ):
            compose(overrides=["++group=a1"])


@mark.usefixtures("hydra_restore_singletons")
@mark.usefixtures("initialize_hydra_no_path")
class TestConfigSearchPathOverride:
    @fixture
    def init_configs(self) -> Any:
        cs = ConfigStore.instance()
        cs.store(
            name="with_sp",
            node={"hydra": {"searchpath": ["pkg://hydra.test_utils.configs"]}},
        )
        cs.store(name="without_sp", node={})

        cs.store(name="bad1", node={"hydra": {"searchpath": 42}})
        cs.store(name="bad2", node={"hydra": {"searchpath": [42]}})

        # Using this triggers an error. Only primary configs are allowed to override hydra.searchpath
        cs.store(
            group="group2",
            name="overriding_sp",
            node={"hydra": {"searchpath": ["abc"]}},
            package="_global_",
        )
        yield

    @mark.parametrize(
        ("config_name", "overrides", "expected"),
        [
            # config group is interpreted as simple config value addition.
            param("without_sp", ["+group1=file1"], {"group1": "file1"}, id="without"),
            param("with_sp", ["+group1=file1"], {"foo": 10}, id="with"),
            # Overriding hydra.searchpath
            param(
                "without_sp",
                ["hydra.searchpath=[pkg://hydra.test_utils.configs]", "+group1=file1"],
                {"foo": 10},
                id="sp_added_by_override",
            ),
            param(
                "with_sp",
                ["hydra.searchpath=[]", "+group1=file1"],
                {"group1": "file1"},
                id="sp_removed_by_override",
            ),
        ],
    )
    def test_searchpath_in_primary_config(
        self,
        init_configs: Any,
        config_name: str,
        overrides: List[str],
        expected: Any,
    ) -> None:
        cfg = compose(config_name=config_name, overrides=overrides)
        assert cfg == expected

    @mark.parametrize(
        ("config_name", "overrides", "expected"),
        [
            param(
                "bad1",
                [],
                raises(
                    ConfigCompositionException,
                    match=re.escape(
                        "hydra.searchpath must be a list of strings. Got: 42"
                    ),
                ),
                id="bad_cp_in_config",
            ),
            param(
                "bad2",
                [],
                raises(
                    ConfigCompositionException,
                    match=re.escape(
                        "hydra.searchpath must be a list of strings. Got: [42]"
                    ),
                ),
                id="bad_cp_element_in_config",
            ),
            param(
                "without_sp",
                ["hydra.searchpath=42"],
                raises(
                    ConfigCompositionException,
                    match=re.escape(
                        "hydra.searchpath must be a list of strings. Got: 42"
                    ),
                ),
                id="bad_override1",
            ),
            param(
                "without_sp",
                ["hydra.searchpath=[42]"],
                raises(
                    ConfigCompositionException,
                    match=re.escape(
                        "hydra.searchpath must be a list of strings. Got: [42]"
                    ),
                ),
                id="bad_override2",
            ),
            param(
                "without_sp",
                ["+group2=overriding_sp"],
                raises(
                    ConfigCompositionException,
                    match=re.escape(
                        "In 'group2/overriding_sp': Overriding hydra.searchpath "
                        "is only supported from the primary config"
                    ),
                ),
                id="overriding_sp_from_non_primary_config",
            ),
        ],
    )
    def test_searchpath_config_errors(
        self,
        init_configs: Any,
        config_name: str,
        overrides: List[str],
        expected: Any,
    ) -> None:
        with expected:
            compose(config_name=config_name, overrides=overrides)
