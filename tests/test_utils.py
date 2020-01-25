# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra import utils
from hydra.core.hydra_config import HydraConfig


def some_method() -> int:
    return 42


class Bar:
    def __init__(self, a: Any, b: Any, c: Any, d: Any) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def static_method() -> int:
        return 43

    def __eq__(self, other: Any) -> Any:
        """Overrides the default implementation"""
        if isinstance(other, Bar):

            return (
                self.a == other.a
                and self.b == other.b
                and self.c == other.c
                and self.d == other.d
            )
        return NotImplemented

    def __ne__(self, other: Any) -> Any:
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented


@pytest.mark.parametrize("path,expected_type", [("tests.test_utils.Bar", Bar)])  # type: ignore
def test_get_class(path: str, expected_type: type) -> None:
    assert utils.get_class(path) == expected_type


@pytest.mark.parametrize("path,return_value", [("tests.test_utils.some_method", 42)])  # type: ignore
def test_get_method(path: str, return_value: Any) -> None:
    assert utils.get_method(path)() == return_value


@pytest.mark.parametrize(  # type: ignore
    "path,return_value", [("tests.test_utils.Bar.static_method", 43)]
)
def test_get_static_method(path: str, return_value: Any) -> None:
    assert utils.get_static_method(path)() == return_value


@pytest.mark.parametrize(  # type: ignore
    "input_conf, key_to_get_config, kwargs_to_pass, expected",
    [
        (
            {
                "class": "tests.test_utils.Bar",
                "params": {"a": 10, "b": 20, "c": 30, "d": 40},
            },
            None,
            {},
            Bar(10, 20, 30, 40),
        ),
        (
            {
                "all_params": {
                    "main": {
                        "class": "tests.test_utils.Bar",
                        "params": {"a": 10, "b": 20, "c": "${all_params.aux.c}"},
                    },
                    "aux": {"c": 30},
                }
            },
            "all_params.main",
            {"d": 40},
            Bar(10, 20, 30, 40),
        ),
        (
            {"class": "tests.test_utils.Bar", "params": {"b": 20, "c": 30}},
            None,
            {"a": 10, "d": 40},
            Bar(10, 20, 30, 40),
        ),
        (
            {"class": "tests.test_utils.Bar", "params": {"b": 200, "c": "${params.b}"}},
            None,
            {"a": 10, "d": 40},
            Bar(10, 200, 200, 40),
        ),
    ],
)
def test_class_instantiate(
    input_conf: Dict[str, Any],
    key_to_get_config: Optional[str],
    kwargs_to_pass: Dict[str, Any],
    expected: Any,
) -> Any:
    conf = OmegaConf.create(input_conf)
    assert isinstance(conf, DictConfig)
    if key_to_get_config is None:
        config_to_pass = conf
    else:
        config_to_pass = conf.select(key_to_get_config)
    obj = utils.instantiate(config_to_pass, **kwargs_to_pass)
    assert obj == expected


def test_get_original_cwd() -> None:
    orig = "/foo/bar"
    cfg = OmegaConf.create({"hydra": {"runtime": {"cwd": orig}}})
    assert isinstance(cfg, DictConfig)
    HydraConfig().set_config(cfg)
    assert utils.get_original_cwd() == orig


@pytest.mark.parametrize(  # type: ignore
    "orig_cwd, path, expected",
    [
        ("/home/omry/hydra", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "/foo/bar", "/foo/bar"),
    ],
)
def test_to_absolute_path(orig_cwd: str, path: str, expected: str) -> None:
    # normalize paths to current OS
    orig_cwd = str(Path(orig_cwd))
    path = str(Path(path))
    expected = str(Path(expected))
    cfg = OmegaConf.create({"hydra": {"runtime": {"cwd": orig_cwd}}})
    assert isinstance(cfg, DictConfig)
    HydraConfig().set_config(cfg)
    assert utils.to_absolute_path(path) == expected
