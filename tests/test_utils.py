# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from pathlib import Path
from typing import Any

from omegaconf import DictConfig, OmegaConf
from pytest import mark, raises

from hydra import utils
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
