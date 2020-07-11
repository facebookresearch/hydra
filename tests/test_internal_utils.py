# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import sys
from typing import Any, Union

import pytest
from _pytest.python_api import RaisesContext  # type: ignore
from omegaconf import DictConfig, OmegaConf

from hydra._internal import utils
from hydra._internal.utils import _locate
from hydra.types import ObjectConf
from tests import AClass, Adam, AnotherClass, ASubclass, NestingClass, Parameters


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
    assert utils.get_column_widths(matrix) == expected


@pytest.mark.parametrize(  # type: ignore
    "config, expected, warning",
    [
        pytest.param(ObjectConf(target="foo"), "foo", False, id="ObjectConf:target"),
        pytest.param(
            OmegaConf.create({"cls": "foo"}), "foo", "cls", id="DictConfig:cls"
        ),
        pytest.param(
            OmegaConf.create({"class": "foo"}), "foo", "class", id="DictConfig:class"
        ),
        pytest.param(
            OmegaConf.create({"target": "foo"}), "foo", False, id="DictConfig:target",
        ),
        pytest.param(
            OmegaConf.create({"cls": "foo", "target": "bar"}),
            "bar",
            False,
            id="DictConfig:cls_target",
        ),
        pytest.param(
            OmegaConf.create({"class": "foo", "target": "bar"}),
            "bar",
            "class",
            id="DictConfig:class_target",
        ),
    ],
)
def test_get_class_name(
    config: Union[ObjectConf, DictConfig], expected: Any, warning: Any, recwarn: Any
) -> None:
    assert utils._get_cls_name(config) == expected
    if warning is not False:
        deprecated = "is deprecated since Hydra 1.0 and will be removed in Hydra 1.1"
        if isinstance(config, DictConfig):
            exp = f"""Config key '{config._get_full_key(warning)}' {deprecated}.
Use 'target' instead of '{warning}'."""
        else:
            exp = f"""
ObjectConf field '{warning}' {deprecated}.
Use 'target' instead of '{warning}'."""

        assert len(recwarn) == 1
        assert recwarn[0].category == UserWarning
        assert recwarn[0].message.args[0] == exp


@pytest.mark.skipif(  # type: ignore
    sys.version_info < (3, 7), reason="requires python3.7"
)
def test_cls() -> None:
    with pytest.warns(expected_warning=UserWarning):
        assert utils._get_cls_name(ObjectConf(cls="foo")) == "foo"
    with pytest.warns(expected_warning=UserWarning):
        assert utils._get_cls_name(ObjectConf(cls="foo", target="bar")) == "bar"


@pytest.mark.parametrize(  # type: ignore
    "name,expected",
    [
        ("tests.Adam", Adam),
        ("tests.Parameters", Parameters),
        ("tests.AClass", AClass),
        ("tests.ASubclass", ASubclass),
        ("tests.NestingClass", NestingClass),
        ("tests.AnotherClass", AnotherClass),
        ("", pytest.raises(ImportError, match=re.escape("Empty path"))),
        (
            "not_found",
            pytest.raises(
                ImportError, match=re.escape("Error loading module 'not_found'")
            ),
        ),
        (
            "tests.b.c.Door",
            pytest.raises(
                ImportError, match=re.escape("Could not locate 'tests.b.c.Door'")
            ),
        ),
    ],
)
def test_locate(name: str, expected: Any) -> None:
    if isinstance(expected, RaisesContext):
        with expected:
            _locate(name)
    else:
        assert _locate(name) == expected
