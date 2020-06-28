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
from tests import (
    AClass,
    Adam,
    AnotherClass,
    ASubclass,
    IllegalType,
    NestingClass,
    Parameters,
)


@pytest.mark.parametrize(  # type: ignore
    "path,expected_type", [("tests.AClass", AClass)]
)
def test_get_class(path: str, expected_type: type) -> None:
    assert utils.get_class(path) == expected_type


@pytest.mark.parametrize(  # type: ignore
    "input_conf, passthrough, expected",
    [
        pytest.param(
            {"target": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}},
            {},
            AClass(10, 20, 30, 40),
            id="class",
        ),
        pytest.param(
            {"target": "tests.AClass", "params": {"b": 20, "c": 30}},
            {"a": 10, "d": 40},
            AClass(10, 20, 30, 40),
            id="class+override",
        ),
        pytest.param(
            {"target": "tests.AClass", "params": {"b": 200, "c": "${params.b}"}},
            {"a": 10, "b": 99, "d": 40},
            AClass(10, 99, 99, 40),
            id="class+override+interpolation",
        ),
        # Check class and static methods
        pytest.param(
            {"target": "tests.ASubclass.class_method", "params": {"y": 10}},
            {},
            ASubclass(11),
            id="class_method",
        ),
        pytest.param(
            {"target": "tests.AClass.static_method", "params": {"z": 43}},
            {},
            43,
            id="static_method",
        ),
        # Check nested types and static methods
        pytest.param(
            {"target": "tests.NestingClass", "params": {}},
            {},
            NestingClass(ASubclass(10)),
            id="class_with_nested_class",
        ),
        pytest.param(
            {"target": "tests.nesting.a.class_method", "params": {"y": 10}},
            {},
            ASubclass(11),
            id="class_method_on_an_object_nested_in_a_global",
        ),
        pytest.param(
            {"target": "tests.nesting.a.static_method", "params": {"z": 43}},
            {},
            43,
            id="static_method_on_an_object_nested_in_a_global",
        ),
        # Check that default value is respected
        pytest.param(
            {"target": "tests.AClass", "params": {"b": 200, "c": "${params.b}"}},
            {"a": 10},
            AClass(10, 200, 200, "default_value"),
            id="instantiate_respects_default_value",
        ),
        pytest.param(
            {"target": "tests.AClass", "params": {}},
            {"a": 10, "b": 20, "c": 30},
            AClass(10, 20, 30, "default_value"),
            id="instantiate_respects_default_value",
        ),
        # call a function from a module
        pytest.param(
            {"target": "tests.module_function", "params": {"x": 43}},
            {},
            43,
            id="call_function_in_module",
        ),
        # Check builtins
        pytest.param(
            {"target": "builtins.str", "params": {"object": 43}},
            {},
            "43",
            id="builtin_types",
        ),
        # passthrough
        pytest.param(
            {"target": "tests.AClass"},
            {"a": 10, "b": 20, "c": 30},
            AClass(a=10, b=20, c=30),
            id="passthrough",
        ),
        pytest.param(
            {"target": "tests.AClass"},
            {"a": 10, "b": 20, "c": 30, "d": {"x": IllegalType()}},
            AClass(a=10, b=20, c=30, d={"x": IllegalType()}),
            id="passthrough",
        ),
    ],
)
def test_class_instantiate(
    input_conf: Any, passthrough: Dict[str, Any], expected: Any,
) -> Any:
    conf = OmegaConf.create(input_conf)
    assert isinstance(conf, DictConfig)
    conf_copy = copy.deepcopy(conf)
    obj = utils.instantiate(conf, **passthrough)
    assert obj == expected
    # make sure config is not modified by instantiate
    assert conf == conf_copy


def test_class_instantiate_pass_omegaconf_node() -> Any:
    conf = OmegaConf.structured(
        ObjectConf(
            target="tests.AClass",
            params={"b": 200, "c": {"x": 10, "y": "${params.b}"}},
        )
    )
    obj = utils.instantiate(conf, **{"a": 10, "d": AnotherClass(99)})
    assert obj == AClass(10, 200, {"x": 10, "y": 200}, AnotherClass(99))
    assert OmegaConf.is_config(obj.c)


def test_instantiate_deprecations() -> None:
    expected = AClass(10, 20, 30, 40)
    with pytest.warns(UserWarning):
        config = OmegaConf.structured(
            {"class": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    with pytest.warns(UserWarning):
        config = OmegaConf.structured(
            {"cls": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    config = OmegaConf.structured(
        {"target": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
    )
    assert utils.instantiate(config) == expected


def test_get_original_cwd(hydra_restore_singletons: Any) -> None:
    orig = "/foo/AClass"
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
    cfg = ObjectConf(target="tests.AClass", params={"a": 10, "b": 20})
    assert utils.instantiate(cfg, c=30) == AClass(a=10, b=20, c=30)
