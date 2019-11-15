# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

import hydra.experimental
from hydra._internal.hydra import GlobalHydra
from hydra.test_utils.test_utils import chdir_hydra_root
from hydra.test_utils.test_utils import does_not_raise

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import hydra_global_context  # noqa: F401

chdir_hydra_root()


def test_initialize_hydra():
    try:
        assert not GlobalHydra().is_initialized()
        hydra.experimental.initialize_hydra(
            task_name="task", search_path_dir=None, strict=True
        )
        assert GlobalHydra().is_initialized()
    finally:
        GlobalHydra().clear()


@pytest.mark.parametrize(
    "search_path_dir", ["hydra/test_utils/configs", "pkg://hydra.test_utils.configs"],
)
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
        search_path_dir,
        config_file,
        overrides,
        expected,
    ):
        with hydra_global_context(search_path_dir=search_path_dir):
            ret = hydra.experimental.compose(config_file, overrides)
            assert ret == expected

    def test_compose_config(
        self,
        search_path_dir,
        hydra_global_context,  # noqa: F811
        config_file,
        overrides,
        expected,
    ):
        with hydra_global_context(search_path_dir=search_path_dir):
            cfg = hydra.experimental.compose(config_file, overrides)
            assert cfg == expected

    def test_strict_failure_global_strict(
        self,
        hydra_global_context,  # noqa: F811
        search_path_dir,
        config_file,
        overrides,
        expected,
    ):
        # default strict True, call is unspecified
        overrides.append("fooooooooo=bar")
        with hydra_global_context(search_path_dir=search_path_dir, strict=True):
            with pytest.raises(KeyError):
                hydra.experimental.compose(config_file, overrides)

    def test_strict_failure_call_is_strict(
        self,
        hydra_global_context,  # noqa: F811
        search_path_dir,
        config_file,
        overrides,
        expected,
    ):
        # default strict false, but call is strict
        with hydra_global_context(search_path_dir=search_path_dir, strict=False):
            with pytest.raises(KeyError):
                hydra.experimental.compose(
                    config_file=config_file, overrides=overrides, strict=True
                )

        # default strict true, but call is false
        with hydra_global_context(search_path_dir=search_path_dir, strict=True):

            with does_not_raise():
                hydra.experimental.compose(
                    config_file=config_file, overrides=overrides, strict=False
                )

    def test_strict_failure_disabled_on_call(
        self,
        hydra_global_context,  # noqa: F811
        search_path_dir,
        config_file,
        overrides,
        expected,
    ):
        # default strict true, but call is false
        with hydra_global_context(search_path_dir=search_path_dir, strict=True):
            with does_not_raise():
                hydra.experimental.compose(
                    config_file=config_file, overrides=overrides, strict=False
                )
