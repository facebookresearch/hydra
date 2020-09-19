# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any

import pytest
from _pytest.python_api import RaisesContext
from omegaconf import DictConfig, OmegaConf

from hydra._internal import utils
from hydra._internal.utils import _locate
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
    "config, expected",
    [
        pytest.param(
            OmegaConf.create({"_target_": "foo"}), "foo", id="ObjectConf:target"
        ),
    ],
)
def test_get_class_name(config: DictConfig, expected: Any) -> None:
    assert utils._get_cls_name(config) == expected


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
            pytest.raises(ImportError, match=re.escape("No module named 'tests.b'")),
        ),
    ],
)
def test_locate(name: str, expected: Any) -> None:
    if isinstance(expected, RaisesContext):
        with expected:
            _locate(name)
    else:
        assert _locate(name) == expected
