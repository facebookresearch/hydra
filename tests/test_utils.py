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
from hydra.errors import InstantiationException
from hydra.types import TargetConf
from tests import (
    AClass,
    Adam,
    AdamConf,
    AnotherClass,
    ASubclass,
    BadAdamConf,
    CenterCrop,
    CenterCropConf,
    Compose,
    ComposeConf,
    IllegalType,
    Mapping,
    MappingConf,
    NestingClass,
    Parameters,
    Rotation,
    RotationConf,
    Tree,
    TreeConf,
    UntypedPassthroughClass,
    UntypedPassthroughConf,
    BClass,
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
    "recursive",
    [
        pytest.param(False, id="non_recursive"),
        pytest.param(True, id="recursive"),
    ],
)
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
            {"_target_": "tests.AClass"},
            {
                "a": 10,
                "b": 20,
                "c": 30,
                "d": {"x": [10, IllegalType()]},
            },
            AClass(a=10, b=20, c=30, d={"x": [10, IllegalType()]}),
            id="passthrough:list",
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
    input_conf: Any, passthrough: Dict[str, Any], expected: Any, recursive: bool
) -> Any:
    def test(conf: Any) -> None:
        passthrough["_recursive_"] = recursive
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


def test_targetconf_deprecated() -> None:
    with pytest.warns(
        expected_warning=UserWarning,
        match=re.escape(
            "TargetConf is deprecated since Hydra 1.1 and will be removed in Hydra 1.2."
        ),
    ):
        TargetConf()


def test_instantiate_bad_adam_conf(recwarn: Any) -> None:
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
        ModuleNotFoundError, match=re.escape("No module named 'some_missing_module'")
    ):
        # can't instantiate when importing a missing module
        utils.instantiate({"_target_": "tests.ClassWithMissingModule"})


def test_pass_extra_variables() -> None:
    cfg = OmegaConf.create({"_target_": "tests.AClass", "a": 10, "b": 20})
    assert utils.instantiate(cfg, c=30) == AClass(a=10, b=20, c=30)


@pytest.mark.parametrize(  # type: ignore
    "cfg, passthrough, expected",
    [
        # direct
        pytest.param(
            {
                "_target_": "tests.Tree",
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 21,
                },
                "right": {
                    "_target_": "tests.Tree",
                    "value": 22,
                },
            },
            {},
            Tree(value=1, left=Tree(value=21), right=Tree(value=22)),
            id="recursive:direct:dict",
        ),
        pytest.param(
            {"_target_": "tests.Tree"},
            {"value": 1},
            Tree(value=1),
            id="recursive:direct:dict:passthrough",
        ),
        pytest.param(
            {"_target_": "tests.Tree"},
            {"value": 1, "left": {"_target_": "tests.Tree", "value": 2}},
            Tree(value=1, left=Tree(2)),
            id="recursive:direct:dict:passthrough",
        ),
        pytest.param(
            {"_target_": "tests.Tree"},
            {
                "value": 1,
                "left": {"_target_": "tests.Tree", "value": 2},
                "right": {"_target_": "tests.Tree", "value": 3},
            },
            Tree(value=1, left=Tree(2), right=Tree(3)),
            id="recursive:direct:dict:passthrough",
        ),
        pytest.param(
            {"_target_": "tests.Tree"},
            {"value": IllegalType()},
            Tree(value=IllegalType()),
            id="recursive:direct:dict:passthrough:incompatible_value",
        ),
        pytest.param(
            {"_target_": "tests.Tree"},
            {"value": 1, "left": {"_target_": "tests.Tree", "value": IllegalType()}},
            Tree(value=1, left=Tree(value=IllegalType())),
            id="recursive:direct:dict:passthrough:incompatible_value",
        ),
        pytest.param(
            TreeConf(
                value=1,
                left=TreeConf(value=21),
                right=TreeConf(value=22),
            ),
            {},
            Tree(value=1, left=Tree(value=21), right=Tree(value=22)),
            id="recursive:direct:dataclass",
        ),
        pytest.param(
            TreeConf(
                value=1,
                left=TreeConf(value=21),
            ),
            {"right": {"value": 22}},
            Tree(value=1, left=Tree(value=21), right=Tree(value=22)),
            id="recursive:direct:dataclass:passthrough",
        ),
        pytest.param(
            TreeConf(
                value=1,
                left=TreeConf(value=21),
            ),
            {"right": TreeConf(value=22)},
            Tree(value=1, left=Tree(value=21), right=Tree(value=22)),
            id="recursive:direct:dataclass:passthrough",
        ),
        pytest.param(
            TreeConf(
                value=1,
                left=TreeConf(value=21),
            ),
            {
                "right": TreeConf(value=IllegalType()),
            },
            Tree(value=1, left=Tree(value=21), right=Tree(value=IllegalType())),
            id="recursive:direct:dataclass:passthrough",
        ),
        # list
        # note that passthrough to a list element is not currently supported
        pytest.param(
            ComposeConf(
                transforms=[
                    CenterCropConf(size=10),
                    RotationConf(degrees=45),
                ]
            ),
            {},
            Compose(
                transforms=[
                    CenterCrop(size=10),
                    Rotation(degrees=45),
                ]
            ),
            id="recursive:list:dataclass",
        ),
        pytest.param(
            {
                "_target_": "tests.Compose",
                "transforms": [
                    {"_target_": "tests.CenterCrop", "size": 10},
                    {"_target_": "tests.Rotation", "degrees": 45},
                ],
            },
            {},
            Compose(
                transforms=[
                    CenterCrop(size=10),
                    Rotation(degrees=45),
                ]
            ),
            id="recursive:list:dict",
        ),
        # map
        pytest.param(
            MappingConf(
                dictionary={
                    "a": MappingConf(),
                    "b": MappingConf(),
                }
            ),
            {},
            Mapping(
                dictionary={
                    "a": Mapping(),
                    "b": Mapping(),
                }
            ),
            id="recursive:map:dataclass",
        ),
        pytest.param(
            {
                "_target_": "tests.Mapping",
                "dictionary": {
                    "a": {"_target_": "tests.Mapping"},
                    "b": {"_target_": "tests.Mapping"},
                },
            },
            {},
            Mapping(
                dictionary={
                    "a": Mapping(),
                    "b": Mapping(),
                }
            ),
            id="recursive:map:dict",
        ),
        pytest.param(
            {
                "_target_": "tests.Mapping",
                "dictionary": {
                    "a": {"_target_": "tests.Mapping"},
                },
            },
            {
                "dictionary": {
                    "b": {"_target_": "tests.Mapping"},
                },
            },
            Mapping(
                dictionary={
                    "a": Mapping(),
                    "b": Mapping(),
                }
            ),
            id="recursive:map:dict:passthrough",
        ),
    ],
)
def test_recursive_instantiation(
    cfg: Any,
    passthrough: Dict[str, Any],
    expected: Any,
) -> None:
    obj = utils.instantiate(cfg, **passthrough)
    assert obj == expected


@pytest.mark.parametrize(  # type: ignore
    "cfg, passthrough, expected",
    [
        pytest.param(
            {
                "_target_": "tests.Tree",
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 21,
                },
            },
            {},
            Tree(value=1, left=Tree(value=21)),
            id="default",
        ),
        pytest.param(
            {
                "_target_": "tests.Tree",
                "_recursive_": True,
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 21,
                },
            },
            {"_recursive_": True},
            Tree(value=1, left=Tree(value=21)),
            id="cfg:true,override:true",
        ),
        pytest.param(
            {
                "_target_": "tests.Tree",
                "_recursive_": True,
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 21,
                },
            },
            {"_recursive_": False},
            Tree(value=1, left={"_target_": "tests.Tree", "value": 21}),
            id="cfg:true,override:false",
        ),
        pytest.param(
            {
                "_target_": "tests.Tree",
                "_recursive_": False,
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 21,
                },
            },
            {"_recursive_": True},
            Tree(value=1, left=Tree(value=21)),
            id="cfg:false,override:true",
        ),
        pytest.param(
            {
                "_target_": "tests.Tree",
                "_recursive_": False,
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 21,
                },
            },
            {"_recursive_": False},
            Tree(value=1, left={"_target_": "tests.Tree", "value": 21}),
            id="cfg:false,override:false",
        ),
        pytest.param(
            {
                "_target_": "tests.Tree",
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 2,
                    "left": {
                        "_target_": "tests.Tree",
                        "value": 3,
                    },
                },
            },
            {},
            Tree(value=1, left=Tree(value=2, left=Tree(value=3))),
            id="3_levels:default",
        ),
        pytest.param(
            {
                "_target_": "tests.Tree",
                "_recursive_": False,
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "value": 2,
                    "left": {
                        "_target_": "tests.Tree",
                        "value": 3,
                    },
                },
            },
            {},
            Tree(
                value=1,
                left={
                    "_target_": "tests.Tree",
                    "value": 2,
                    "left": {"_target_": "tests.Tree", "value": 3},
                },
            ),
            id="3_levels:cfg1=false",
        ),
        pytest.param(
            {
                "_target_": "tests.Tree",
                "value": 1,
                "left": {
                    "_target_": "tests.Tree",
                    "_recursive_": False,
                    "value": 2,
                    "left": {
                        "_target_": "tests.Tree",
                        "value": 3,
                    },
                },
            },
            {},
            Tree(
                value=1, left=Tree(value=2, left={"_target_": "tests.Tree", "value": 3})
            ),
            id="3_levels:cfg2=false",
        ),
    ],
)
def test_recursive_override(
    cfg: Any,
    passthrough: Any,
    expected: Any,
) -> None:
    obj = utils.instantiate(cfg, **passthrough)
    assert obj == expected


@pytest.mark.parametrize(  # type: ignore
    "input_conf, passthrough, expected",
    [
        pytest.param(
            {"_target_": "tests.AClass", "a": 10, "b": 20, "c": 30, "d": 40},
            {"_target_": "tests.BClass"},
            BClass(10, 20, 30, 40),
            id="override_same_args",
        ),
        pytest.param(
            {"_target_": "tests.AClass", "a": 10, "b": 20},
            {"_target_": "tests.BClass"},
            BClass(10, 20, "c", "d"),
            id="override_other_args",
        ),
        pytest.param(
            {
                "_target_": "tests.AClass",
                "a": 10,
                "b": 20,
                "c": {"_target_": "tests.AClass", "a": "aa", "b": "bb", "c": "cc"},
            },
            {"_target_": "tests.BClass"},
            BClass(10, 20, AClass(a="aa", b="bb", c="cc"), "d"),
            id="recursive_no_override",
        ),
        pytest.param(
            {
                "_target_": "tests.AClass",
                "a": 10,
                "b": 20,
                "c": {"_target_": "tests.AClass", "a": "aa", "b": "bb", "c": "cc"},
            },
            {"_target_": "tests.BClass", "c": {"_target_": "tests.BClass"}},
            BClass(10, 20, BClass(a="aa", b="bb", c="cc"), "d"),
            id="recursive_override",
        ),
    ],
)
def test_override_target(input_conf, passthrough, expected):
    conf_copy = copy.deepcopy(input_conf)
    obj = utils.instantiate(input_conf, **passthrough)
    assert obj == expected
    # make sure config is not modified by instantiate
    assert input_conf == conf_copy
