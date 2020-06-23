# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Optional

import pytest
from omegaconf import OmegaConf

from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.config_search_path import SearchPathQuery
from hydra.core.global_hydra import GlobalHydra
from hydra.errors import HydraException
from hydra.experimental import (
    compose,
    initialize,
    initialize_config_dir,
    initialize_config_dir_ctx,
    initialize_config_module,
    initialize_config_module_ctx,
    initialize_ctx,
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
        SearchPathQuery(provider="main", search_path=None)
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
        self, config_path: str, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_ctx(config_path=config_path):
            cfg = compose(config_file, overrides)
            assert cfg == expected

    def test_strict_failure_global_strict(
        self, config_path: str, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_ctx(config_path=config_path):
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
        initialize(config_path=None, strict=True)


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
        self, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_ctx(config_path="../examples/jupyter_notebooks/cloud/conf"):
            ret = compose(config_file, overrides)
            assert ret == expected

    def test_initialize_config_dir_ctx_with_relative_dir(
        self, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_config_dir_ctx(
            config_dir="../examples/jupyter_notebooks/cloud/conf", job_name="job_name"
        ):
            ret = compose(config_file, overrides)
            assert ret == expected

    def test_initialize_config_module_ctx(
        self, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_config_module_ctx(
            config_module="examples.jupyter_notebooks.conf", job_name="job_name"
        ):
            ret = compose(config_file, overrides)
            assert ret == expected


def test_initialize_config_dir_ctz_with_absolute_dir(tmpdir: Any,) -> None:
    tmpdir = Path(tmpdir)
    (tmpdir / "test_group").mkdir(parents=True)
    cfg = OmegaConf.create({"foo": "bar"})

    cfg_file = tmpdir / "test_group" / "test.yaml"
    with open(str(cfg_file), "w") as f:
        f.write("# @package _group_\n")
        OmegaConf.save(cfg, f)

    with initialize_config_dir_ctx(config_dir=str(tmpdir)):
        ret = compose(overrides=["+test_group=test"])
        assert ret == {"test_group": cfg}


@pytest.mark.usefixtures("hydra_restore_singletons")
@pytest.mark.parametrize(
    "job_name,expected", [(None, "test_compose"), ("test_job", "test_job")]
)
class TestInitJobNameOverride:
    def test_initialize_ctx(self, job_name: Optional[str], expected: str) -> None:
        with initialize_ctx(
            config_path="../examples/jupyter_notebooks/cloud/conf", job_name=job_name
        ):
            ret = compose(return_hydra_config=True)
            assert ret.hydra.job.name == expected

    def test_initialize_config_dir_ctx(
        self, job_name: Optional[str], expected: str
    ) -> None:
        with initialize_config_dir_ctx(
            config_dir="../examples/jupyter_notebooks/cloud/conf", job_name=job_name
        ):
            ret = compose(return_hydra_config=True)
            assert ret.hydra.job.name == expected


def test_initialize_config_module_ctx(hydra_restore_singletons: Any) -> None:
    with initialize_config_module_ctx(config_module="examples.jupyter_notebooks.conf"):
        ret = compose(return_hydra_config=True)
        assert ret.hydra.job.name == "app"

    with initialize_config_module_ctx(
        config_module="examples.jupyter_notebooks.conf", job_name="test_job"
    ):
        ret = compose(return_hydra_config=True)
        assert ret.hydra.job.name == "test_job"


def test_missing_init_py_error(hydra_restore_singletons: Any) -> None:
    with pytest.raises(
        Exception,
        match=re.escape(
            "Unexpected error checking content of 'hydra.test_utils.configs.missing_init_py', "
            "did you forget an __init__.py?"
        ),
    ):
        with initialize_ctx(config_path="../hydra/test_utils/configs/missing_init_py"):
            hydra = GlobalHydra.instance().hydra
            assert hydra is not None
            hydra.compose_config(config_name=None, overrides=[])


def test_initialize_config_dir(hydra_restore_singletons: Any) -> None:
    initialize_config_dir(
        config_dir="test_apps/app_with_cfg_groups/conf", job_name="my_app"
    )
    assert compose(config_name="config") == {
        "optimizer": {"type": "nesterov", "lr": 0.001}
    }


def test_initialize_with_module(hydra_restore_singletons: Any) -> None:
    initialize_config_module(
        config_module="tests.test_apps.app_with_cfg_groups.conf", job_name="my_pp"
    )
    assert compose(config_name="config") == {
        "optimizer": {"type": "nesterov", "lr": 0.001}
    }


def test_hydra_main_passthrough(hydra_restore_singletons: Any) -> None:
    initialize_config_dir(
        config_dir="test_apps/app_with_cfg_groups/conf", job_name="my_app"
    )
    from tests.test_apps.app_with_cfg_groups.my_app import my_app  # type: ignore

    cfg = compose(config_name="config", overrides=["optimizer.lr=1.0"])
    assert my_app(cfg) == {"optimizer": {"type": "nesterov", "lr": 1.0}}


def test_initialization_root_module(monkeypatch: Any) -> None:
    subprocess.check_call(
        [sys.executable, "tests/test_apps/test_initializations/root_module/main.py"],
    )

    monkeypatch.chdir("tests/test_apps/test_initializations/root_module")
    subprocess.check_call([sys.executable, "-m", "main"])
