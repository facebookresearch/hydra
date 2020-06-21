# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any, List

import pytest

from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra.core.config_search_path import SearchPathQuery
from hydra.core.global_hydra import GlobalHydra
from hydra.errors import HydraException
from hydra.experimental import (
    compose,
    initialize,
    initialize_ctx,
    initialize_with_file,
    initialize_with_file_ctx,
    initialize_with_module,
    initialize_with_module_ctx,
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
    def test_compose__initialize_auto(
        self, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_ctx(config_path="../examples/jupyter_notebooks/conf"):
            ret = compose(config_file, overrides)
            assert ret == expected

    def test_compose__init_with_file(
        self, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_with_file_ctx(
            file="examples/jupyter_notebooks/fake_file", config_path="conf"
        ):
            ret = compose(config_file, overrides)
            assert ret == expected

    def test_compose__init_with_module(
        self, config_file: str, overrides: List[str], expected: Any,
    ) -> None:
        with initialize_with_module_ctx(
            module="examples.jupyter_notebooks.fake_module", config_path="conf"
        ):
            ret = compose(config_file, overrides)
            assert ret == expected


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


def test_initialize_with_file(hydra_restore_singletons: Any) -> None:
    initialize_with_file(
        file="tests/test_apps/app_with_cfg_groups/my_app.py", config_path="conf"
    )
    assert compose(config_name="config") == {
        "optimizer": {"type": "nesterov", "lr": 0.001}
    }


def test_initialize_with_module(hydra_restore_singletons: Any) -> None:
    initialize_with_module(
        module="tests.test_apps.app_with_cfg_groups.my_app", config_path="conf"
    )
    assert compose(config_name="config") == {
        "optimizer": {"type": "nesterov", "lr": 0.001}
    }


def test_hydra_main_passthrough(hydra_restore_singletons: Any) -> None:
    initialize_with_file(
        file="tests/test_apps/app_with_cfg_groups/my_app.py", config_path="conf"
    )
    from tests.test_apps.app_with_cfg_groups.my_app import my_app

    cfg = compose(config_name="config", overrides=["optimizer.lr=0.1"])
    assert my_app(cfg) == {"optimizer": {"type": "nesterov", "lr": 0.1}}
