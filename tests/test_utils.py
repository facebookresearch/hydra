# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
from omegaconf import MISSING, DictConfig, ListConfig, OmegaConf

from hydra import utils
from hydra._internal.utils import _convert_container_targets_to_strings
from hydra.conf import HydraConf, RuntimeConf
from hydra.core.hydra_config import HydraConfig
from hydra.errors import InstantiationException
from hydra.types import TargetConf
from hydra.utils import ConvertMode
from tests import (
    AClass,
    Adam,
    AdamConf,
    AnotherClass,
    ASubclass,
    BadAdamConf,
    BClass,
    CenterCrop,
    CenterCropConf,
    Compose,
    ComposeConf,
    IllegalType,
    Mapping,
    MappingConf,
    NestedConf,
    NestingClass,
    Parameters,
    Rotation,
    RotationConf,
    SimpleClass,
    SimpleClassDefaultPrimitiveConf,
    SimpleClassNonPrimitiveConf,
    SimpleClassPrimitiveConf,
    SimpleDataClass,
    Tree,
    TreeConf,
    UntypedPassthroughClass,
    UntypedPassthroughConf,
    User,
    module_function,
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


def test_interpolation_is_live_in_instantiated_object() -> None:
    """
    Interpolations in instantiated objects are live config objects but not for primitive objects.
    """
    cfg = OmegaConf.create(
        {
            "node": {
                "_target_": "tests.AClass",
                "a": "${value}",
                "b": {"x": "${value}"},
                "c": 30,
                "d": 40,
            },
            "value": 99,
        }
    )
    obj = utils.instantiate(cfg.node)
    assert obj.a == 99
    assert obj.b.x == 99

    cfg.value = 3.14

    # interpolation is not live for primitive objects
    assert obj.a == 99  # unchanged
    # but is live for config objects
    assert obj.b.x == 3.14


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
    expected = Adam(lr=0.123, params=adam_params)
    assert res.params == expected.params
    assert res.lr == expected.lr
    assert list(res.betas) == list(expected.betas)  # OmegaConf converts tuples to lists
    assert res.eps == expected.eps
    assert res.weight_decay == expected.weight_decay
    assert res.amsgrad == expected.amsgrad


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
            id="str:override_same_args",
        ),
        pytest.param(
            {"_target_": "tests.AClass", "a": 10, "b": 20, "c": 30, "d": 40},
            {"_target_": BClass},
            BClass(10, 20, 30, 40),
            id="type:override_same_args",
        ),
        pytest.param(
            {"_target_": "tests.AClass", "a": 10, "b": 20},
            {"_target_": "tests.BClass"},
            BClass(10, 20, "c", "d"),
            id="str:override_other_args",
        ),
        pytest.param(
            {"_target_": "tests.AClass", "a": 10, "b": 20},
            {"_target_": BClass},
            BClass(10, 20, "c", "d"),
            id="type:override_other_args",
        ),
        pytest.param(
            {
                "_target_": "tests.AClass",
                "a": 10,
                "b": 20,
                "c": {
                    "_target_": "tests.AClass",
                    "a": "aa",
                    "b": "bb",
                    "c": "cc",
                },
            },
            {
                "_target_": "tests.BClass",
                "c": {
                    "_target_": "tests.BClass",
                },
            },
            BClass(10, 20, BClass(a="aa", b="bb", c="cc"), "d"),
            id="str:recursive_override",
        ),
        pytest.param(
            {
                "_target_": "tests.AClass",
                "a": 10,
                "b": 20,
                "c": {
                    "_target_": "tests.AClass",
                    "a": "aa",
                    "b": "bb",
                    "c": "cc",
                },
            },
            {"_target_": BClass, "c": {"_target_": BClass}},
            BClass(10, 20, BClass(a="aa", b="bb", c="cc"), "d"),
            id="type:recursive_override",
        ),
    ],
)
def test_override_target(input_conf: Any, passthrough: Any, expected: Any) -> None:
    conf_copy = copy.deepcopy(input_conf)
    obj = utils.instantiate(input_conf, **passthrough)
    assert obj == expected
    # make sure config is not modified by instantiate
    assert input_conf == conf_copy


@pytest.mark.parametrize(  # type: ignore
    "input_, expected",
    [
        pytest.param({"a": 10}, {"a": 10}),
        pytest.param([1, 2, 3], [1, 2, 3]),
        pytest.param({"_target_": "abc", "a": 10}, {"_target_": "abc", "a": 10}),
        pytest.param(
            {"_target_": AClass, "a": 10}, {"_target_": "tests.AClass", "a": 10}
        ),
        pytest.param(
            {"_target_": AClass.static_method, "a": 10},
            {"_target_": "tests.AClass.static_method", "a": 10},
        ),
        pytest.param(
            {"_target_": ASubclass.class_method, "a": 10},
            {"_target_": "tests.ASubclass.class_method", "a": 10},
        ),
        pytest.param(
            {"_target_": module_function, "a": 10},
            {"_target_": "tests.module_function", "a": 10},
        ),
        pytest.param(
            {
                "_target_": AClass,
                "a": {"_target_": AClass, "b": 10},
            },
            {
                "_target_": "tests.AClass",
                "a": {"_target_": "tests.AClass", "b": 10},
            },
        ),
        pytest.param(
            [1, {"_target_": AClass, "a": 10}],
            [1, {"_target_": "tests.AClass", "a": 10}],
        ),
    ],
)
def test_convert_target_to_string(input_: Any, expected: Any) -> None:
    _convert_container_targets_to_strings(input_)
    assert input_ == expected


@pytest.mark.parametrize(  # type: ignore
    "primitive,expected_primitive",
    [
        pytest.param(None, False, id="unspecified"),
        pytest.param(ConvertMode.NONE, False, id="none"),
        pytest.param(ConvertMode.PARTIAL, True, id="partial"),
        pytest.param(ConvertMode.ALL, True, id="all"),
    ],
)
@pytest.mark.parametrize(  # type: ignore
    "input_,expected",
    [
        pytest.param(
            {
                "obj": {
                    "_target_": "tests.AClass",
                    "a": {"foo": "bar"},
                    "b": OmegaConf.create({"foo": "bar"}),
                    "c": [1, 2, 3],
                    "d": OmegaConf.create([1, 2, 3]),
                },
            },
            AClass(
                a={"foo": "bar"},
                b={"foo": "bar"},
                c=[1, 2, 3],
                d=[1, 2, 3],
            ),
            id="simple",
        ),
        pytest.param(
            {
                "value": 99,
                "obj": {
                    "_target_": "tests.AClass",
                    "a": {"foo": "${value}"},
                    "b": OmegaConf.create({"foo": "${value}"}),
                    "c": [1, "${value}"],
                    "d": OmegaConf.create([1, "${value}"]),
                },
            },
            AClass(
                a={"foo": 99},
                b={"foo": 99},
                c=[1, 99],
                d=[1, 99],
            ),
            id="interpolation",
        ),
    ],
)
def test_convert_params_override(
    primitive: Optional[bool], expected_primitive: bool, input_: Any, expected: Any
) -> None:
    input_cfg = OmegaConf.create(input_)
    if primitive is not None:
        ret = utils.instantiate(input_cfg.obj, _convert_=primitive)
    else:
        ret = utils.instantiate(input_cfg.obj)

    expected_list: Any
    expected_dict: Any
    if expected_primitive is True:
        expected_list = list
        expected_dict = dict
    else:
        expected_list = ListConfig
        expected_dict = DictConfig

    assert ret == expected
    assert isinstance(ret.a, expected_dict)
    assert isinstance(ret.b, expected_dict)
    assert isinstance(ret.c, expected_list)
    assert isinstance(ret.d, expected_list)


@pytest.mark.parametrize(  # type: ignore
    "convert_mode",
    [  # type: ignore
        pytest.param(None, id="none"),
        pytest.param(ConvertMode.NONE, id="none"),
        pytest.param(ConvertMode.PARTIAL, id="partial"),
        pytest.param(ConvertMode.ALL, id="all"),
    ],
)
@pytest.mark.parametrize(  # type: ignore
    "input_,expected",
    [
        pytest.param(
            {
                "value": 99,
                "obj": {
                    "_target_": "tests.SimpleClass",
                    "a": {
                        "_target_": "tests.SimpleClass",
                        "a": {"foo": "${value}"},
                        "b": [1, "${value}"],
                    },
                    "b": None,
                },
            },
            SimpleClass(a={"foo": 99}, b=[1, 99]),
            id="simple",
        ),
    ],
)
def test_convert_params(input_: Any, expected: Any, convert_mode: Any):
    cfg = OmegaConf.create(input_)
    ret = utils.instantiate(
        cfg.obj,
        **{
            "a": {"_convert_": convert_mode},
        },
    )

    if convert_mode in (ConvertMode.PARTIAL, ConvertMode.ALL):
        assert isinstance(ret.a.a, dict)
        assert isinstance(ret.a.b, list)
    elif convert_mode in (None, ConvertMode.NONE):
        assert isinstance(ret.a.a, DictConfig)
        assert isinstance(ret.a.b, ListConfig)
    else:
        assert False

    assert ret.a == expected


@pytest.mark.parametrize(  # type: ignore
    "convert",
    [  # type: ignore
        pytest.param(None, id="p=unspecified"),
        pytest.param(ConvertMode.NONE, id="none"),
        pytest.param(ConvertMode.PARTIAL, id="partial"),
        pytest.param(ConvertMode.ALL, id="all"),
    ],
)
@pytest.mark.parametrize(  # type: ignore
    "input_,expected",
    [
        pytest.param(
            {
                "value": 99,
                "obj": {
                    "_target_": "tests.SimpleDataClass",
                    "a": {
                        "_target_": "tests.SimpleDataClass",
                        "a": {"foo": "${value}"},
                        "b": [1, "${value}"],
                    },
                    "b": None,
                },
            },
            SimpleDataClass(a={"foo": 99}, b=[1, 99]),
            id="simple",
        ),
    ],
)
def test_convert_params_with_dataclass_obj(input_: Any, expected: Any, convert: Any):
    # Instantiated dataclasses are never converted to primitives.
    # This is due to the ambiguity between dataclass as an object and as
    # an input for creating a config object (Structured Configs)
    # Even in ConvertMode.ALL - the underlying dict and list are converted to DictConfig and ListConfig
    # because the parent DictConfig cannot hold unwrapped list and dict.
    # This behavior is unique to instantiated objects that are dataclasses.

    cfg = OmegaConf.create(input_)
    kwargs = {"a": {"_convert_": convert}}
    ret = utils.instantiate(cfg.obj, **kwargs)

    assert ret.a == expected
    # as close as it gets for dataclasses:
    # Object is a DictConfig and the underlying type is the expected type.
    assert isinstance(ret.a, DictConfig) and OmegaConf.get_type(ret.a) == type(expected)
    # Since these are nested in , they are not getting converted. not the greatest behavior.
    # Can potentially be solved if this is causing issues.
    assert isinstance(ret.a.a, DictConfig)
    assert isinstance(ret.a.b, ListConfig)


@pytest.mark.parametrize(  # type: ignore
    "input_,is_primitive,expected",
    [
        pytest.param(
            {
                "value": 99,
                "obj": SimpleClassPrimitiveConf(
                    a={"foo": "${value}"}, b=[1, "${value}"]
                ),
            },
            True,
            SimpleClass(a={"foo": 99}, b=[1, 99]),
            id="primitive_specified_true",
        ),
        pytest.param(
            {
                "value": 99,
                "obj": SimpleClassNonPrimitiveConf(
                    a={"foo": "${value}"}, b=[1, "${value}"]
                ),
            },
            False,
            SimpleClass(a={"foo": 99}, b=[1, 99]),
            id="primitive_specified_false",
        ),
        pytest.param(
            {
                "value": 99,
                "obj": SimpleClassDefaultPrimitiveConf(
                    a={"foo": "${value}"}, b=[1, "${value}"]
                ),
            },
            False,
            SimpleClass(a={"foo": 99}, b=[1, 99]),
            id="default_behavior",
        ),
    ],
)
def test_convert_in_config(input_: Any, is_primitive: bool, expected: Any) -> None:
    cfg = OmegaConf.create(input_)
    ret = utils.instantiate(cfg.obj)
    assert ret == expected

    if is_primitive:
        assert isinstance(ret.a, dict)
        assert isinstance(ret.b, list)
    else:
        assert isinstance(ret.a, DictConfig)
        assert isinstance(ret.b, ListConfig)


def test_nested_dataclass_with_partial_convert() -> None:
    # dict
    cfg = OmegaConf.structured(NestedConf)
    ret = utils.instantiate(cfg, _convert_="partial")
    assert isinstance(ret.a, DictConfig) and OmegaConf.get_type(ret.a) == User
    assert isinstance(ret.b, DictConfig) and OmegaConf.get_type(ret.b) == User
    expected = SimpleClass(a=User(name="a", age=1), b=User(name="b", age=2))
    assert ret == expected

    # list
    lst = [User(name="a", age=1)]
    cfg = OmegaConf.structured(NestedConf(a=lst))
    ret = utils.instantiate(cfg, _convert_="partial")
    assert isinstance(ret.a, list) and OmegaConf.get_type(ret.a[0]) == User
    assert isinstance(ret.b, DictConfig) and OmegaConf.get_type(ret.b) == User
    expected = SimpleClass(a=lst, b=User(name="b", age=2))
    assert ret == expected


class DictValues:
    def __init__(self, d: Dict[str, User]):
        self.d = d


class ListValues:
    def __init__(self, d: List[User]):
        self.d = d


def test_dict_with_structured_config() -> None:
    @dataclass
    class DictValuesConf:
        _target_: str = "tests.test_utils.DictValues"
        d: Dict[str, User] = MISSING

    schema = OmegaConf.structured(DictValuesConf)
    cfg = OmegaConf.merge(schema, {"d": {"007": {"name": "Bond", "age": 7}}})
    obj = utils.instantiate(config=cfg, _convert_="none")
    assert OmegaConf.is_dict(obj.d)
    assert OmegaConf.get_type(obj.d["007"]) == User

    obj = utils.instantiate(config=cfg, _convert_="partial")
    assert isinstance(obj.d, dict)
    assert OmegaConf.get_type(obj.d["007"]) == User

    obj = utils.instantiate(config=cfg, _convert_="all")
    assert isinstance(obj.d, dict)
    assert isinstance(obj.d["007"], dict)


def test_list_with_structured_config() -> None:
    @dataclass
    class ListValuesConf:
        _target_: str = "tests.test_utils.ListValues"
        d: List[User] = MISSING

    schema = OmegaConf.structured(ListValuesConf)
    cfg = OmegaConf.merge(schema, {"d": [{"name": "Bond", "age": 7}]})

    obj = utils.instantiate(config=cfg, _convert_="none")
    assert isinstance(obj.d, ListConfig)
    assert OmegaConf.get_type(obj.d[0]) == User

    obj = utils.instantiate(config=cfg, _convert_="partial")
    assert isinstance(obj.d, list)
    assert OmegaConf.get_type(obj.d[0]) == User

    obj = utils.instantiate(config=cfg, _convert_="all")
    assert isinstance(obj.d, list)
    assert isinstance(obj.d[0], dict)


def test_list_as_none() -> None:
    @dataclass
    class ListValuesConf:
        _target_: str = "tests.test_utils.ListValues"
        d: Optional[List[User]] = None

    cfg = OmegaConf.structured(ListValuesConf)
    obj = utils.instantiate(config=cfg)
    assert obj.d is None
