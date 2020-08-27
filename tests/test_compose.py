# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Optional

import pytest
from omegaconf import OmegaConf
from pytest import raises

from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.config_search_path import SearchPathQuery
from hydra.core.global_hydra import GlobalHydra
from hydra.errors import HydraException
from hydra.experimental import (
    compose,
    initialize,
    initialize_config_dir,
    initialize_config_module,
)
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


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


@pytest.mark.usefixtures("hydra_restore_singletons")
@pytest.mark.parametrize("config_path", ["../hydra/test_utils/configs"])
@pytest.mark.parametrize(
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
        self, config_path: str, config_file: str, overrides: List[str], expected: Any
    ) -> None:
        with initialize(config_path=config_path):
            cfg = compose(config_file, overrides)
            assert cfg == expected

    def test_strict_failure_global_strict(
        self, config_path: str, config_file: str, overrides: List[str], expected: Any
    ) -> None:
        with initialize(config_path=config_path):
            # default strict True, call is unspecified
            overrides.append("fooooooooo=bar")
            with pytest.raises(HydraException):
                compose(config_file, overrides)


def test_strict_deprecation_warning(hydra_restore_singletons: Any) -> None:
    msg = (
        "\n@hydra.main(strict) flag is deprecated and will removed in the next version."
        "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/strict_mode_flag_deprecated"
    )
    with pytest.warns(expected_warning=UserWarning, match=re.escape(msg)):
        try:
            initialize(config_path=None, strict=True)
        finally:
            GlobalHydra.instance().clear()


@pytest.mark.usefixtures("hydra_restore_singletons")
@pytest.mark.parametrize(
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
        with pytest.raises(
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
        f.write("# @package _group_\n")
        OmegaConf.save(cfg, f)

    with initialize_config_dir(config_dir=str(tmpdir)):
        ret = compose(overrides=["+test_group=test"])
        assert ret == {"test_group": cfg}


@pytest.mark.parametrize(  # type: ignore
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

    with pytest.raises(Exception, match=re.escape(expected)):
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

    with pytest.raises(Exception, match=re.escape(expected)):
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
