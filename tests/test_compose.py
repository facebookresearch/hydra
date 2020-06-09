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
    initialize_with_file,
    initialize_with_module,
)
from hydra.test_utils.test_utils import (
    TGlobalHydraContext,
    chdir_hydra_root,
    does_not_raise,
)

chdir_hydra_root()


def test_initialize(restore_singletons: Any) -> None:
    assert not GlobalHydra().is_initialized()
    initialize(config_path=None)
    assert GlobalHydra().is_initialized()


def test_initialize_with_config_dir(restore_singletons: Any) -> None:
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


@pytest.mark.usefixtures("restore_singletons")
@pytest.mark.parametrize("config_dir", ["../hydra/test_utils/configs"])
@pytest.mark.parametrize(
    "config_file, overrides, expected",
    [
        (None, [], {}),
        (None, ["+foo=bar"], {"foo": "bar"}),
        ("compose.yaml", [], {"foo": 10, "bar": 100}),
        ("compose.yaml", ["group1=file2"], {"foo": 20, "bar": 100}),
    ],
)
class TestCompose:
    def test_compose_decorator(
        self,
        hydra_global_context: TGlobalHydraContext,
        config_dir: str,
        config_file: str,
        overrides: List[str],
        expected: Any,
    ) -> None:
        with hydra_global_context(config_dir=config_dir):
            ret = compose(config_file, overrides)
            assert ret == expected

    def test_compose_config(
        self,
        config_dir: str,
        hydra_global_context: TGlobalHydraContext,
        config_file: str,
        overrides: List[str],
        expected: Any,
    ) -> None:
        with hydra_global_context(config_dir=config_dir):
            cfg = compose(config_file, overrides)
            assert cfg == expected

    def test_strict_failure_global_strict(
        self,
        config_dir: str,
        hydra_global_context: TGlobalHydraContext,
        config_file: str,
        overrides: List[str],
        expected: Any,
    ) -> None:
        # default strict True, call is unspecified
        overrides.append("fooooooooo=bar")
        with hydra_global_context(config_dir=config_dir):
            with pytest.raises(HydraException):
                compose(config_file, overrides)

    def test_strict_failure_call_is_strict(
        self,
        config_dir: str,
        hydra_global_context: TGlobalHydraContext,
        config_file: str,
        overrides: List[str],
        expected: Any,
        recwarn: Any,
    ) -> None:
        # default strict false, but call is strict
        with hydra_global_context(config_dir=config_dir, strict=False):
            with pytest.raises(HydraException):
                compose(config_name=config_file, overrides=overrides, strict=True)

        # default strict true, but call is false
        with hydra_global_context(config_dir=config_dir, strict=True):

            with does_not_raise():
                compose(config_name=config_file, overrides=overrides, strict=False)

    def test_strict_failure_disabled_on_call(
        self,
        config_dir: str,
        hydra_global_context: TGlobalHydraContext,
        config_file: str,
        overrides: List[str],
        expected: Any,
        recwarn: Any,
    ) -> None:
        # default strict true, but call is false
        with hydra_global_context(config_dir=config_dir, strict=True):
            with does_not_raise():
                compose(config_name=config_file, overrides=overrides, strict=False)


def test_strict_deprecation_warning(restore_singletons: Any) -> None:
    msg = (
        "\n@hydra.main(strict) flag is deprecated and will removed in the next version."
        "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/strict_mode_flag_deprecated"
    )
    with pytest.warns(expected_warning=UserWarning, match=re.escape(msg)):
        initialize(config_path=None, strict=True)


@pytest.mark.usefixtures("restore_singletons")
@pytest.mark.parametrize(
    "config_dir", ["../hydra/test_utils/configs/cloud_infra_example"]
)
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
        # load file
        (
            "config.yaml",
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
            "config.yaml",
            ["environment=production", "db=mysql"],
            {
                "db": {"driver": "mysql", "user": "mysql", "pass": "r4Zn*jQ9JB1Rz2kfz"},
                "cloud": {"name": "local", "host": "localhost", "port": 9876},
            },
        ),
    ],
)
class TestComposeCloudInfraExample:
    def test_compose(
        self,
        config_dir: str,
        hydra_global_context: TGlobalHydraContext,
        config_file: str,
        overrides: List[str],
        expected: Any,
    ) -> None:
        with hydra_global_context(config_dir=config_dir):
            ret = compose(config_file, overrides)
            assert ret == expected


def test_missing_init_py_error(
    restore_singletons: Any, hydra_global_context: TGlobalHydraContext
) -> None:
    with pytest.raises(
        Exception,
        match=re.escape(
            "Unexpected error checking content of 'hydra.test_utils.configs.missing_init_py', "
            "did you forget an __init__.py?"
        ),
    ):
        with hydra_global_context(
            config_dir="../hydra/test_utils/configs/missing_init_py"
        ):
            hydra = GlobalHydra.instance().hydra
            assert hydra is not None
            hydra.compose_config(config_name=None, overrides=[])


def test_initialize_with_file(restore_singletons: Any) -> None:
    initialize_with_file(
        calling_file="tests/test_apps/app_with_cfg_groups/my_app.py", config_path="conf"
    )
    assert compose(config_name="config") == {
        "optimizer": {"type": "nesterov", "lr": 0.001}
    }


def test_initialize_with_module(restore_singletons: Any) -> None:
    initialize_with_module(
        calling_module="tests.test_apps.app_with_cfg_groups.my_app", config_path="conf"
    )
    assert compose(config_name="config") == {
        "optimizer": {"type": "nesterov", "lr": 0.001}
    }


def test_hydra_main_passthrough(restore_singletons: Any) -> None:
    initialize_with_file(
        calling_file="tests/test_apps/app_with_cfg_groups/my_app.py", config_path="conf"
    )
    from tests.test_apps.app_with_cfg_groups.my_app import my_app

    cfg = compose(config_name="config", overrides=["optimizer.lr=0.1"])
    assert my_app(cfg) == {"optimizer": {"type": "nesterov", "lr": 0.1}}
