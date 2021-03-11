# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any

from _pytest.python_api import RaisesContext, raises
from pytest import mark

from hydra._internal.utils import _locate
from hydra.utils import get_class
from tests.instantiate import (
    AClass,
    Adam,
    AnotherClass,
    ASubclass,
    NestingClass,
    Parameters,
)


@mark.parametrize(
    "name,expected",
    [
        ("tests.instantiate.Adam", Adam),
        ("tests.instantiate.Parameters", Parameters),
        ("tests.instantiate.AClass", AClass),
        ("tests.instantiate.ASubclass", ASubclass),
        ("tests.instantiate.NestingClass", NestingClass),
        ("tests.instantiate.AnotherClass", AnotherClass),
        ("", raises(ImportError, match=re.escape("Empty path"))),
        [
            "not_found",
            raises(ImportError, match=re.escape("Error loading module 'not_found'")),
        ],
        (
            "tests.instantiate.b.c.Door",
            raises(
                ImportError, match=re.escape("No module named 'tests.instantiate.b'")
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


@mark.parametrize("path,expected_type", [("tests.instantiate.AClass", AClass)])
def test_get_class(path: str, expected_type: type) -> None:
    assert get_class(path) == expected_type
