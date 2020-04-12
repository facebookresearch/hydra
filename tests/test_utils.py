# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
from omegaconf import DictConfig, OmegaConf

import hydra._internal.utils as internal_utils
from hydra import utils
from hydra.conf import HydraConf, RuntimeConf
from hydra.core.hydra_config import HydraConfig
from hydra.types import ObjectConf


def some_method() -> int:
    return 42


class Bar:
    def __init__(self, a: Any, b: Any, c: Any, d: Any = "default_value") -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __repr__(self) -> str:
        return f"a={self.a}, b={self.b}, c={self.c}, d={self.d}"

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


class Foo:
    def __init__(self, x: int) -> None:
        self.x = x

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, Foo):
            return self.x == other.x
        return False


class Baz(Foo):
    @classmethod
    def class_method(self, y: int) -> Any:
        return self(y + 1)

    @staticmethod
    def static_method(z: int) -> int:
        return z


class Fii:
    def __init__(self, a: Baz = Baz(10)):
        self.a = a

    def __repr__(self) -> str:
        return f"a={self.a}"

    def __eq__(self, other: Any) -> Any:
        """Overrides the default implementation"""
        if isinstance(other, Fii):

            return self.a == other.a
        return NotImplemented

    def __ne__(self, other: Any) -> Any:
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented


fii = Fii()


def fum(k: int) -> int:
    return k + 1


@pytest.mark.parametrize(  # type: ignore
    "path,expected_type", [("tests.test_utils.Bar", Bar)]
)
def test_get_class(path: str, expected_type: type) -> None:
    assert utils.get_class(path) == expected_type


@pytest.mark.parametrize(  # type: ignore
    "path,return_value", [("tests.test_utils.some_method", 42)]
)
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
                "cls": "tests.test_utils.Bar",
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
                        "cls": "tests.test_utils.Bar",
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
            {"cls": "tests.test_utils.Bar", "params": {"b": 20, "c": 30}},
            None,
            {"a": 10, "d": 40},
            Bar(10, 20, 30, 40),
        ),
        (
            {"cls": "tests.test_utils.Bar", "params": {"b": 200, "c": "${params.b}"}},
            None,
            {"a": 10, "d": 40},
            Bar(10, 200, 200, 40),
        ),
        # Check class and static methods
        (
            {"cls": "tests.test_utils.Baz.class_method", "params": {"y": 10}},
            None,
            {},
            Baz(11),
        ),
        (
            {"cls": "tests.test_utils.Baz.static_method", "params": {"z": 43}},
            None,
            {},
            43,
        ),
        # Check nested types and static methods
        ({"cls": "tests.test_utils.Fii", "params": {}}, None, {}, Fii(Baz(10)),),
        (
            {"cls": "tests.test_utils.fii.a.class_method", "params": {"y": 10}},
            None,
            {},
            Baz(11),
        ),
        (
            {"cls": "tests.test_utils.fii.a.static_method", "params": {"z": 43}},
            None,
            {},
            43,
        ),
        # Check that default value is respected
        (
            {"cls": "tests.test_utils.Bar", "params": {"b": 200, "c": "${params.b}"}},
            None,
            {"a": 10},
            Bar(10, 200, 200, "default_value"),
        ),
        (
            {"cls": "tests.test_utils.Bar", "params": {}},
            None,
            {"a": 10, "b": 20, "c": 30},
            Bar(10, 20, 30, "default_value"),
        ),
        # call a function from a module
        ({"cls": "tests.test_utils.fum", "params": {"k": 43}}, None, {}, 44,),
        # Check builtins
        ({"cls": "builtins.str", "params": {"object": 43}}, None, {}, "43",),
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
        config_to_pass = OmegaConf.select(conf, key_to_get_config)
    config_to_pass_copy = copy.deepcopy(config_to_pass)
    obj = utils.instantiate(config_to_pass, **kwargs_to_pass)
    assert obj == expected
    # make sure config is not modified by instantiate
    assert config_to_pass == config_to_pass_copy


def test_class_instantiate_pass_omegaconf_node() -> Any:
    pc = ObjectConf()
    # This is a bit clunky because it exposes a problem with the backport of dataclass on Python 3.6
    # see: https://github.com/ericvsmith/dataclasses/issues/155
    pc.cls = "tests.test_utils.Bar"
    pc.params = {"b": 200, "c": {"x": 10, "y": "${params.b}"}}
    conf = OmegaConf.structured(pc)
    obj = utils.instantiate(conf, **{"a": 10, "d": Foo(99)})
    assert obj == Bar(10, 200, {"x": 10, "y": 200}, Foo(99))
    assert OmegaConf.is_config(obj.c)


def test_class_warning() -> None:
    expected = Bar(10, 20, 30, 40)
    with pytest.warns(UserWarning):
        config = OmegaConf.structured(
            {
                "class": "tests.test_utils.Bar",
                "params": {"a": 10, "b": 20, "c": 30, "d": 40},
            }
        )
        assert utils.instantiate(config) == expected

    config = OmegaConf.structured(
        {"cls": "tests.test_utils.Bar", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
    )
    assert utils.instantiate(config) == expected


def test_get_original_cwd(restore_singletons: Any) -> None:
    orig = "/foo/bar"
    cfg = OmegaConf.create({"hydra": HydraConf(runtime=RuntimeConf(cwd=orig))})
    assert isinstance(cfg, DictConfig)
    HydraConfig.instance().set_config(cfg)
    assert utils.get_original_cwd() == orig


def test_get_original_cwd_without_hydra(restore_singletons: Any) -> None:
    with pytest.raises(ValueError):
        utils.get_original_cwd()


@pytest.mark.parametrize(  # type: ignore
    "orig_cwd, path, expected",
    [
        ("/home/omry/hydra", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "/foo/bar", "/foo/bar"),
    ],
)
def test_to_absolute_path(
    restore_singletons: Any, orig_cwd: str, path: str, expected: str
) -> None:
    # normalize paths to current OS
    orig_cwd = str(Path(orig_cwd))
    path = str(Path(path))
    expected = str(Path(expected))
    cfg = OmegaConf.create({"hydra": HydraConf(runtime=RuntimeConf(cwd=orig_cwd))})
    assert isinstance(cfg, DictConfig)
    HydraConfig().set_config(cfg)
    assert utils.to_absolute_path(path) == expected


@pytest.mark.parametrize(  # type: ignore
    "path, expected",
    [
        ("foo/bar", f"{os.getcwd()}/foo/bar"),
        ("foo/bar", f"{os.getcwd()}/foo/bar"),
        ("/foo/bar", os.path.abspath("/foo/bar")),
    ],
)
def test_to_absolute_path_without_hydra(
    restore_singletons: Any, path: str, expected: str
) -> None:
    # normalize paths to current OS
    path = str(Path(path))
    expected = str(Path(expected).absolute())
    assert utils.to_absolute_path(path) == expected


@pytest.mark.parametrize(  # type: ignore
    "matrix,expected",
    [
        ([["a"]], [1]),
        ([["a", "bb"]], [1, 2]),
        ([["a", "bb"], ["aa", "b"]], [2, 2]),
        ([["a"], ["aa", "b"]], [2, 1]),
        ([["a", "aa"], ["bb"]], [2, 2]),
        ([["a"]], [1]),
        ([["a"]], [1]),
        ([["a"]], [1]),
    ],
)
def test_get_column_widths(matrix: Any, expected: Any) -> None:
    assert internal_utils.get_column_widths(matrix) == expected
