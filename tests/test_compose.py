# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

import hydra.experimental
from hydra._internal.hydra import GlobalHydra
from hydra._internal.config_search_path import SearchPath
from hydra.test_utils.test_utils import chdir_hydra_root
from hydra.test_utils.test_utils import does_not_raise

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import hydra_global_context  # noqa: F401

chdir_hydra_root()


def test_initialize():
    try:
        assert not GlobalHydra().is_initialized()
        hydra.experimental.initialize(config_dir=None, strict=True)
        assert GlobalHydra().is_initialized()
    finally:
        GlobalHydra().clear()


def test_initialize_with_config_dir():
    try:
        assert not GlobalHydra().is_initialized()
        hydra.experimental.initialize(
            config_dir="../hydra/test_utils/configs", strict=True
        )
        assert GlobalHydra().is_initialized()

        config_search_path = GlobalHydra().hydra.config_loader.config_search_path
        idx = config_search_path.find_first_match(
            SearchPath(provider="main", search_path=None)
        )
        assert idx != -1
    finally:
        GlobalHydra().clear()


@pytest.mark.parametrize("config_dir", ["../hydra/test_utils/configs"])
@pytest.mark.parametrize(
    "config_file, overrides, expected",
    [
        (None, [], {}),
        (None, ["foo=bar"], {"foo": "bar"}),
        ("compose.yaml", [], {"foo": 10, "bar": 100}),
        ("compose.yaml", ["group1=file2"], {"foo": 20, "bar": 100}),
    ],
)
class TestCompose:
    def test_compose_decorator(
        self,
        hydra_global_context,  # noqa: F811
        config_dir,
        config_file,
        overrides,
        expected,
    ):
        with hydra_global_context(config_dir=config_dir):
            ret = hydra.experimental.compose(config_file, overrides)
            assert ret == expected

    def test_compose_config(
        self,
        config_dir,
        hydra_global_context,  # noqa: F811
        config_file,
        overrides,
        expected,
    ):
        with hydra_global_context(config_dir=config_dir):
            cfg = hydra.experimental.compose(config_file, overrides)
            assert cfg == expected

    def test_strict_failure_global_strict(
        self,
        hydra_global_context,  # noqa: F811
        config_dir,
        config_file,
        overrides,
        expected,
    ):
        # default strict True, call is unspecified
        overrides.append("fooooooooo=bar")
        with hydra_global_context(config_dir=config_dir, strict=True):
            with pytest.raises(KeyError):
                hydra.experimental.compose(config_file, overrides)

    def test_strict_failure_call_is_strict(
        self,
        hydra_global_context,  # noqa: F811
        config_dir,
        config_file,
        overrides,
        expected,
    ):
        # default strict false, but call is strict
        with hydra_global_context(config_dir=config_dir, strict=False):
            with pytest.raises(KeyError):
                hydra.experimental.compose(
                    config_file=config_file, overrides=overrides, strict=True
                )

        # default strict true, but call is false
        with hydra_global_context(config_dir=config_dir, strict=True):

            with does_not_raise():
                hydra.experimental.compose(
                    config_file=config_file, overrides=overrides, strict=False
                )

    def test_strict_failure_disabled_on_call(
        self,
        hydra_global_context,  # noqa: F811
        config_dir,
        config_file,
        overrides,
        expected,
    ):
        # default strict true, but call is false
        with hydra_global_context(config_dir=config_dir, strict=True):
            with does_not_raise():
                hydra.experimental.compose(
                    config_file=config_file, overrides=overrides, strict=False
                )


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
            ["db=sqlite"],
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
            ["db=mysql", "environment=production"],
            {"db": {"driver": "mysql", "user": "mysql", "pass": "r4Zn*jQ9JB1Rz2kfz"}},
        ),
        (
            None,
            ["db=mysql", "environment=production", "application=donkey"],
            {
                "db": {"driver": "mysql", "user": "mysql", "pass": "r4Zn*jQ9JB1Rz2kfz"},
                "donkey": {"name": "kong", "rank": "king"},
            },
        ),
        (
            None,
            [
                "db=mysql",
                "environment=production",
                "application=donkey",
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
        hydra_global_context,  # noqa: F811
        config_dir,
        config_file,
        overrides,
        expected,
    ):
        with hydra_global_context(config_dir=config_dir):
            ret = hydra.experimental.compose(config_file, overrides)
            assert ret == expected
