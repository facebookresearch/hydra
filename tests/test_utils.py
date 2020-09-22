# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os
import re
from pathlib import Path
from typing import Any, Dict

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra import utils
from hydra.conf import HydraConf, RuntimeConf
from hydra.core.hydra_config import HydraConfig
from hydra.errors import HydraException, InstantiationException
from hydra.types import ObjectConf
from tests import (
    AClass,
    Adam,
    AdamConf,
    AnotherClass,
    ASubclass,
    BadAdamConf,
    IllegalType,
    NestingClass,
    Parameters,
    UntypedPassthroughClass,
    UntypedPassthroughConf,
)

objectconf_depreacted = (
    "\nObjectConf is deprecated in favor of TargetConf since Hydra 1.0.0rc3 and will be removed in Hydra 1.1."
    "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
)

target_field_deprecated = (
    "\nConfig key '{field}' is deprecated since Hydra 1.0 and will be removed in Hydra 1.1."
    "\nUse '_target_' instead of '{field}'."
    "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
)

params_field_deprecated = (
    "\nField 'params' is deprecated since Hydra 1.0 and will be removed in Hydra 1.1."
    "\nInline the content of params directly at the containing node."
    "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
)


@pytest.mark.parametrize(  # type: ignore
    "path,expected_type", [("tests.AClass", AClass)]
)
def test_get_class(path: str, expected_type: type) -> None:
    assert utils.get_class(path) == expected_type


def test_a_class_eq() -> None:
    assert AClass(a=10, b=20, c=30, d=40) != AClass(a=11, b=12, c=13, d=14)
    assert AClass(a=10, b=20, c=30, d=40) == AClass(a=10, b=20, c=30, d=40)


@pytest.mark.parametrize(  # type: ignore
    "input_conf, passthrough, expected",
    [
        pytest.param(
            {"_target_": "tests.AClass", "a": 10, "b": 20, "c": 30, "d": 40},
            {},
            AClass(10, 20, 30, 40),
            id="class",
        ),
        pytest.param(
            {"_target_": "tests.AClass", "b": 20, "c": 30},
            {"a": 10, "d": 40},
            AClass(10, 20, 30, 40),
            id="class+override",
        ),
        pytest.param(
            {"_target_": "tests.AClass", "b": 200, "c": "${b}"},
            {"a": 10, "b": 99, "d": 40},
            AClass(10, 99, 99, 40),
            id="class+override+interpolation",
        ),
        # Check class and static methods
        pytest.param(
            {"_target_": "tests.ASubclass.class_method", "y": 10},
            {},
            ASubclass(11),
            id="class_method",
        ),
        pytest.param(
            {"_target_": "tests.AClass.static_method", "z": 43},
            {},
            43,
            id="static_method",
        ),
        # Check nested types and static methods
        pytest.param(
            {"_target_": "tests.NestingClass"},
            {},
            NestingClass(ASubclass(10)),
            id="class_with_nested_class",
        ),
        pytest.param(
            {"_target_": "tests.nesting.a.class_method", "y": 10},
            {},
            ASubclass(11),
            id="class_method_on_an_object_nested_in_a_global",
        ),
        pytest.param(
            {"_target_": "tests.nesting.a.static_method", "z": 43},
            {},
            43,
            id="static_method_on_an_object_nested_in_a_global",
        ),
        # Check that default value is respected
        pytest.param(
            {"_target_": "tests.AClass"},
            {"a": 10, "b": 20, "c": 30},
            AClass(10, 20, 30, "default_value"),
            id="instantiate_respects_default_value",
        ),
        # call a function from a module
        pytest.param(
            {"_target_": "tests.module_function", "x": 43},
            {},
            43,
            id="call_function_in_module",
        ),
        # Check builtins
        pytest.param(
            {"_target_": "builtins.str", "object": 43},
            {},
            "43",
            id="builtin_types",
        ),
        # Check that none is instantiated correctly
        pytest.param(None, {}, None, id="instantiate_none"),
        # passthrough
        pytest.param(
            {"_target_": "tests.AClass"},
            {"a": 10, "b": 20, "c": 30},
            AClass(a=10, b=20, c=30),
            id="passthrough",
        ),
        pytest.param(
            {"_target_": "tests.AClass"},
            {"a": 10, "b": 20, "c": 30, "d": {"x": IllegalType()}},
            AClass(a=10, b=20, c=30, d={"x": IllegalType()}),
            id="passthrough",
        ),
        pytest.param(
            UntypedPassthroughConf,
            {"a": IllegalType()},
            UntypedPassthroughClass(a=IllegalType()),
            id="untyped_passthrough",
        ),
    ],
)
def test_class_instantiate(
    input_conf: Any, passthrough: Dict[str, Any], expected: Any
) -> Any:
    def test(conf: Any) -> None:
        conf_copy = copy.deepcopy(conf)
        obj = utils.instantiate(conf, **passthrough)
        assert obj == expected
        # make sure config is not modified by instantiate
        assert conf == conf_copy

    test(input_conf)
    test(OmegaConf.create(input_conf))


@pytest.mark.parametrize(  # type: ignore
    "input_conf, passthrough, expected",
    [
        pytest.param(
            {
                "node": {
                    "_target_": "tests.AClass",
                    "a": "${value}",
                    "b": 20,
                    "c": 30,
                    "d": 40,
                },
                "value": 99,
            },
            {},
            AClass(99, 20, 30, 40),
            id="interpolation_into_parent",
        ),
    ],
)
def test_interpolation_accessing_parent(
    input_conf: Any, passthrough: Dict[str, Any], expected: Any
) -> Any:
    input_conf = OmegaConf.create(input_conf)
    obj = utils.instantiate(input_conf.node, **passthrough)
    assert obj == expected


@pytest.mark.parametrize(  # type: ignore
    "input_conf, passthrough, expected",
    [
        pytest.param(
            {"_target_": "tests.AClass", "params": {"b": 200, "c": "${params.b}"}},
            {"a": 10},
            AClass(10, 200, 200, "default_value"),
            id="instantiate_respects_default_value",
        )
    ],
)
def test_instantiate_respects_default_value_with_params(
    input_conf: Any, passthrough: Dict[str, Any], expected: Any, recwarn: Any
) -> Any:
    conf = OmegaConf.create(input_conf)
    assert isinstance(conf, DictConfig)
    conf_copy = copy.deepcopy(conf)
    obj = utils.instantiate(conf, **passthrough)
    assert obj == expected
    # make sure config is not modified by instantiate
    assert conf == conf_copy


def test_class_instantiate_objectconf_pass_omegaconf_node() -> Any:
    with pytest.warns(expected_warning=UserWarning) as recwarn:
        conf = OmegaConf.structured(
            ObjectConf(
                target="tests.AClass",
                params={"b": 200, "c": {"x": 10, "y": "${params.b}"}},
            )
        )
        obj = utils.instantiate(conf, **{"a": 10, "d": AnotherClass(99)})
    assert obj == AClass(10, 200, {"x": 10, "y": 200}, AnotherClass(99))
    assert OmegaConf.is_config(obj.c)

    assert recwarn[0].message.args[0] == objectconf_depreacted
    assert recwarn[1].message.args[0] == target_field_deprecated.format(field="target")


def test_class_instantiate_omegaconf_node() -> Any:
    conf = OmegaConf.structured(
        {
            "_target_": "tests.AClass",
            "b": 200,
            "c": {"x": 10, "y": "${b}"},
        }
    )
    obj = utils.instantiate(conf, a=10, d=AnotherClass(99))
    assert obj == AClass(a=10, b=200, c={"x": 10, "y": 200}, d=AnotherClass(99))
    assert OmegaConf.is_config(obj.c)


def test_instantiate_deprecations() -> None:
    expected = AClass(10, 20, 30, 40)
    with pytest.warns(UserWarning, match=target_field_deprecated.format(field="class")):
        config = OmegaConf.structured(
            {"class": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    with pytest.warns(UserWarning, match=target_field_deprecated.format(field="cls")):
        config = OmegaConf.structured(
            {"cls": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    with pytest.warns(
        UserWarning, match=target_field_deprecated.format(field="target")
    ):
        config = OmegaConf.structured(
            {"target": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    with pytest.warns(UserWarning, match=params_field_deprecated):
        config = OmegaConf.structured(
            {"_target_": "tests.AClass", "params": {"a": 10, "b": 20, "c": 30, "d": 40}}
        )
        assert utils.instantiate(config) == expected

    # normal case, no warnings
    config = OmegaConf.structured(
        {"_target_": "tests.AClass", "a": 10, "b": 20, "c": 30, "d": 40}
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


def test_instantiate_adam_objectconf() -> None:
    with pytest.warns(expected_warning=UserWarning, match=objectconf_depreacted):
        with pytest.raises(Exception):
            # can't instantiate without passing params
            utils.instantiate(ObjectConf(target="tests.Adam"))

        adam_params = Parameters([1, 2, 3])
        res = utils.instantiate(ObjectConf(target="tests.Adam"), params=adam_params)
        assert res == Adam(params=adam_params)


def test_instantiate_adam() -> None:
    with pytest.raises(Exception):
        # can't instantiate without passing params
        utils.instantiate({"_target_": "tests.Adam"})

    adam_params = Parameters([1, 2, 3])
    res = utils.instantiate({"_target_": "tests.Adam"}, params=adam_params)
    assert res == Adam(params=adam_params)


def test_instantiate_adam_conf() -> None:
    with pytest.raises(Exception):
        # can't instantiate without passing params
        utils.instantiate({"_target_": "tests.Adam"})

    adam_params = Parameters([1, 2, 3])
    res = utils.instantiate(AdamConf(lr=0.123), params=adam_params)
    assert res == Adam(lr=0.123, params=adam_params)


def test_instantiate_bad_adam_conf() -> None:
    msg = (
        "Missing value for BadAdamConf._target_. Check that it's properly annotated and overridden."
        "\nA common problem is forgetting to annotate _target_ as a string : '_target_: str = ...'"
    )
    with pytest.raises(
        InstantiationException,
        match=re.escape(msg),
    ):
        utils.instantiate(BadAdamConf())


def test_instantiate_with_missing_module() -> None:

    with pytest.raises(
        HydraException, match=re.escape("No module named 'some_missing_module'")
    ):
        # can't instantiate when importing a missing module
        utils.instantiate({"_target_": "tests.ClassWithMissingModule"})


def test_pass_extra_variables() -> None:
    cfg = OmegaConf.create({"_target_": "tests.AClass", "a": 10, "b": 20})
    assert utils.instantiate(cfg, c=30) == AClass(a=10, b=20, c=30)


def test_pass_extra_variables_objectconf() -> None:
    with pytest.warns(expected_warning=UserWarning) as recwarn:
        cfg = ObjectConf(target="tests.AClass", params={"a": 10, "b": 20})
        assert utils.instantiate(cfg, c=30) == AClass(a=10, b=20, c=30)

    assert recwarn[0].message.args[0] == objectconf_depreacted
    assert recwarn[1].message.args[0] == target_field_deprecated.format(field="target")


##################################
# Testing deprecated logic below #
##################################


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
        # Check that none is instantiated correctly
        pytest.param(
            None,
            {},
            None,
            id="instantiate_none",
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
def test_class_instantiate_deprecated(
    input_conf: Any, passthrough: Dict[str, Any], expected: Any, recwarn: Any
) -> Any:
    conf = OmegaConf.create(input_conf)
    assert isinstance(conf, DictConfig)
    conf_copy = copy.deepcopy(conf)
    obj = utils.instantiate(conf, **passthrough)
    assert obj == expected
    # make sure config is not modified by instantiate
    assert conf == conf_copy


def test_object_conf_deprecated() -> None:
    with pytest.warns(UserWarning) as recwarn:
        cfg = ObjectConf(target="tests.AClass", params={"a": 10, "b": 20})
        ret = utils.instantiate(cfg, c=30)
    assert ret == AClass(a=10, b=20, c=30)
    assert recwarn[0].message.args[0] == objectconf_depreacted
    assert recwarn[1].message.args[0] == target_field_deprecated.format(field="target")


@pytest.mark.parametrize(  # type: ignore
    "input_conf, passthrough, expected",
    [
        pytest.param(
            {
                "node": {
                    "cls": "tests.AClass",
                    "params": {"a": "${value}", "b": 20, "c": 30, "d": 40},
                },
                "value": 99,
            },
            {},
            AClass(99, 20, 30, 40),
            id="deprecated:interpolation_into_parent",
        ),
    ],
)
def test_interpolation_accessing_parent_deprecated(
    input_conf: Any, passthrough: Dict[str, Any], expected: Any, recwarn: Any
) -> Any:
    input_conf = OmegaConf.create(input_conf)
    obj = utils.instantiate(input_conf.node, **passthrough)
    assert obj == expected
