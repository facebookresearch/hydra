# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any

from _pytest.python_api import RaisesContext, raises
from pytest import mark, param

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
        param(
            "int",
            raises(ImportError, match=re.escape("Error loading module 'int'")),
            id="int",
        ),
        param("builtins.int", int, id="builtins_explicit"),
        param("builtins.int.from_bytes", int.from_bytes, id="method_of_builtin"),
        param(
            "builtins.int.not_found",
            raises(
                ImportError,
                match=re.escape(
                    "Encountered AttributeError while loading 'builtins.int.not_found':"
                    + " type object 'int' has no attribute 'not_found'"
                ),
            ),
            id="builtin_attribute_error",
        ),
        param(
            "datetime",
            raises(
                ValueError,
                match=re.escape("Invalid type (<class 'module'>) found for datetime"),
            ),
            id="top_level_module",
        ),
        ("tests.instantiate.Adam", Adam),
        ("tests.instantiate.Parameters", Parameters),
        ("tests.instantiate.AClass", AClass),
        param(
            "tests.instantiate.AClass.static_method",
            AClass.static_method,
            id="staticmethod",
        ),
        param(
            "tests.instantiate.AClass.not_found",
            raises(
                ImportError,
                match=re.escape(
                    "Encountered AttributeError while loading 'tests.instantiate.AClass.not_found':"
                    + " type object 'AClass' has no attribute 'not_found'"
                ),
            ),
            id="class_attribute_error",
        ),
        ("tests.instantiate.ASubclass", ASubclass),
        ("tests.instantiate.NestingClass", NestingClass),
        ("tests.instantiate.AnotherClass", AnotherClass),
        ("", raises(ImportError, match=re.escape("Empty path"))),
        (
            "not_found",
            raises(ImportError, match=re.escape("Error loading module 'not_found'")),
        ),
        param(
            "tests.instantiate.b.c.Door",
            raises(
                ImportError,
                match=re.escape(
                    "Encountered AttributeError while loading 'tests.instantiate.b.c.Door':"
                    + " module 'tests.instantiate' has no attribute 'b'"
                ),
            ),
            id="nested_not_found",
        ),
        param(
            "tests.instantiate.import_error",
            raises(
                ImportError,
                match=re.escape(
                    "Error loading 'tests.instantiate.import_error': 'AssertionError()'"
                ),
            ),
            id="import_assertion_error",
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
