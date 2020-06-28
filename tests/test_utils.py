# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os
from pathlib import Path
from typing import Any, Dict

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra import utils
from hydra.conf import HydraConf, RuntimeConf
from hydra.core.hydra_config import HydraConfig
from hydra.types import ObjectConf
from tests import Adam, Bar, Baz, Fii, Foo, Parameters


@pytest.mark.parametrize(  # type: ignore
    "path,expected_type", [("tests.Bar", Bar)]
)
def test_get_class(path: str, expected_type: type) -> None:
    assert utils.get_class(path) == expected_type


@pytest.mark.parametrize(  # type: ignore
    "path,return_value", [("tests.some_method", 42)]
)
def test_get_method(path: str, return_value: Any) -> None:
    assert utils.get_method(path)() == return_value


@pytest.mark.parametrize(  # type: ignore
    "path,return_value", [("tests.Bar.static_method", 43)]
)
def test_get_static_method(path: str, return_value: Any) -> None:
    assert utils.get_static_method(path)() == return_value


@pytest.mark.parametrize(  # type: ignore
    "input_conf, kwargs_to_pass, expected",
    [
        pytest.param(
            {"target": "tests.Bar", "params": {"a": 10, "b": 20, "c": 30, "d": 40}},
            {},
            Bar(10, 20, 30, 40),
            id="class",
        ),
        pytest.param(
            {"target": "tests.Bar", "params": {"b": 20, "c": 30}},
            {"a": 10, "d": 40},
            Bar(10, 20, 30, 40),
            id="class+override",
        ),
        pytest.param(
            {"target": "tests.Bar", "params": {"b": 200, "c": "${params.b}"}},
            {"a": 10, "b": 99, "d": 40},
            Bar(10, 99, 99, 40),
            id="class+override+interpolation",
        ),
        # Check class and static methods
        pytest.param(
            {"target": "tests.Baz.class_method", "params": {"y": 10}},
            {},
            Baz(11),
            id="class_method",
        ),
        pytest.param(
            {"target": "tests.Baz.static_method", "params": {"z": 43}},
            {},
            43,
            id="static_method",
        ),
        # Check nested types and static methods
        pytest.param(
            {"target": "tests.Fii", "params": {}},
            {},
            Fii(Baz(10)),
            id="class_with_nested_class",
        ),
        pytest.param(
            {"target": "tests.fii.a.class_method", "params": {"y": 10}},
            {},
            Baz(11),
            id="class_method_on_an_object_nested_in_a_global",
        ),
        pytest.param(
            {"target": "tests.fii.a.static_method", "params": {"z": 43}},
            {},
            43,
            id="static_method_on_an_object_nested_in_a_global",
        ),
        # Check that default value is respected
        pytest.param(
            {"target": "tests.Bar", "params": {"b": 200, "c": "${params.b}"}},
            {"a": 10},
            Bar(10, 200, 200, "default_value"),
            id="instantiate_respects_default_value",
        ),
        pytest.param(
            {"target": "tests.Bar", "params": {}},
            {"a": 10, "b": 20, "c": 30},
            Bar(10, 20, 30, "default_value"),
            id="instantiate_respects_default_value",
        ),
        # call a function from a module
        pytest.param(
            {"target": "tests.fum", "params": {"k": 43}},
            {},
            44,
            id="call_function_in_module",
        ),
        # Check builtins
        pytest.param(
            {"target": "builtins.str", "params": {"object": 43}},
            {},
            "43",
            id="builtin_types",
        ),
    ],
)
def test_class_instantiate(
    input_conf: Any, kwargs_to_pass: Dict[str, Any], expected: Any,
) -> Any:
    conf = OmegaConf.create(input_conf)
    assert isinstance(conf, DictConfig)
    conf_copy = copy.deepcopy(conf)
    obj = utils.instantiate(conf, **kwargs_to_pass)
    assert obj == expected
    # make sure config is not modified by instantiate
    assert conf == conf_copy


def test_class_instantiate_pass_omegaconf_node() -> Any:
    conf = OmegaConf.structured(
        ObjectConf(
            target="tests.Bar", params={"b": 200, "c": {"x": 10, "y": "${params.b}"}},
        )
    )
    obj = utils.instantiate(conf, **{"a": 10, "d": Foo(99)})
    assert obj == Bar(10, 200, {"x": 10, "y": 200}, Foo(99))
    assert OmegaConf.is_config(obj.c)


def test_class_warning() -> None:
    expected = Bar(10, 20, 30, 40)
    with pytest.warns(UserWarning):
        config = OmegaConf.structured(
            {"class": "tests.Bar", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    with pytest.warns(UserWarning):
        config = OmegaConf.structured(
            {"cls": "tests.Bar", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    config = OmegaConf.structured(
        {"target": "tests.Bar", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
    )
    assert utils.instantiate(config) == expected


def test_get_original_cwd(hydra_restore_singletons: Any) -> None:
    orig = "/foo/bar"
    cfg = OmegaConf.create({"hydra": HydraConf(runtime=RuntimeConf(cwd=orig))})
    assert isinstance(cfg, DictConfig)
    HydraConfig.instance().set_config(cfg)
    assert utils.get_original_cwd() == orig


def test_get_original_cwd_without_hydra(hydra_restore_singletons: Any) -> None:
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


@pytest.mark.parametrize(  # type: ignore
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


def test_instantiate_adam() -> None:
    with pytest.raises(Exception):
        # can't instantiate without passing params
        utils.instantiate(ObjectConf(target="tests.Adam"))

    adam_params = Parameters([1, 2, 3])
    res = utils.instantiate(ObjectConf(target="tests.Adam"), params=adam_params)
    assert res == Adam(params=adam_params)


def test_pass_extra_variables() -> None:
    cfg = ObjectConf(target="tests.Bar", params={"a": 10, "b": 20})
    assert utils.instantiate(cfg, c=30) == Bar(a=10, b=20, c=30)
