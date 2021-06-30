# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import re
from pathlib import Path
from typing import Any, Optional

from omegaconf import DictConfig, OmegaConf
from pytest import mark, param, raises, warns

from hydra import utils
from hydra._internal.utils2 import deprecation_warning
from hydra.conf import HydraConf, RuntimeConf
from hydra.core.hydra_config import HydraConfig


def test_get_original_cwd(hydra_restore_singletons: Any) -> None:
    orig = "/foo/AClass"
    cfg = OmegaConf.create({"hydra": HydraConf(runtime=RuntimeConf(cwd=orig))})
    assert isinstance(cfg, DictConfig)
    HydraConfig.instance().set_config(cfg)
    assert utils.get_original_cwd() == orig


def test_get_original_cwd_without_hydra(hydra_restore_singletons: Any) -> None:
    with raises(ValueError):
        utils.get_original_cwd()


@mark.parametrize(
    "orig_cwd, path, expected",
    [
        ("/home/omry/hydra", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "/foo/bar", "/foo/bar"),
    ],
)
def test_to_absolute_path(
    hydra_restore_singletons: Any, orig_cwd: str, path: str, expected: str
) -> None:
    # normalize paths to current OS
    orig_cwd = str(Path(orig_cwd))
    path = str(Path(path))
    expected = str(Path(expected))
    cfg = OmegaConf.create({"hydra": HydraConf(runtime=RuntimeConf(cwd=orig_cwd))})
    assert isinstance(cfg, DictConfig)
    HydraConfig().set_config(cfg)
    assert utils.to_absolute_path(path) == expected


@mark.parametrize(
    "path, expected",
    [
        ("foo/bar", f"{os.getcwd()}/foo/bar"),
        ("foo/bar", f"{os.getcwd()}/foo/bar"),
        ("/foo/bar", os.path.abspath("/foo/bar")),
    ],
)
def test_to_absolute_path_without_hydra(
    hydra_restore_singletons: Any, path: str, expected: str
) -> None:
    # normalize paths to current OS
    path = str(Path(path))
    expected = str(Path(expected).absolute())
    assert utils.to_absolute_path(path) == expected


@mark.parametrize(
    "env_setting,expected_error",
    [
        param(None, False, id="env_unset"),
        param("", False, id="env_empty"),
        param("1", True, id="env_set"),
    ],
)
def test_deprecation_warning(
    monkeypatch: Any, env_setting: Optional[str], expected_error: bool
) -> None:
    msg = "Feature FooBar is deprecated"
    if env_setting is not None:
        monkeypatch.setenv("HYDRA_DEPRECATION_WARNINGS_AS_ERRORS", env_setting)
    if expected_error:
        with raises(DeprecationWarning, match=re.escape(msg)):
            deprecation_warning(msg)
    else:
        with warns(UserWarning, match=re.escape(msg)):
            deprecation_warning(msg)
