# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest
from hydra import utils
from omegaconf import OmegaConf


def some_method():
    return 42


class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @staticmethod
    def static_method():
        return 43

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Foo):
            return self.a == other.a and self.b == other.b
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented


class Bar:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def static_method():
        return 43

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Bar):
            return (
                self.a == other.a
                and self.b == other.b
                and self.c == other.c
                and self.d == other.d
            )
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented


@pytest.mark.parametrize("path,expected_type", [("tests.test_utils.Foo", Foo)])
def test_get_class(path, expected_type):
    assert utils.get_class(path) == expected_type


@pytest.mark.parametrize("path,return_value", [("tests.test_utils.some_method", 42)])
def test_get_method(path, return_value):
    assert utils.get_method(path)() == return_value


@pytest.mark.parametrize(
    "path,return_value", [("tests.test_utils.Foo.static_method", 43)]
)
def test_get_static_method(path, return_value):
    assert utils.get_static_method(path)() == return_value


@pytest.mark.parametrize(
    "conf, expected",
    [({"class": "tests.test_utils.Foo", "params": {"a": 10, "b": 20}}, Foo(10, 20))],
)
def test_class_instantiate(conf, expected):
    conf = OmegaConf.create(conf)
    obj = utils.instantiate(conf)
    assert obj == expected


@pytest.mark.parametrize(
    "conf, expected",
    [
        (
            {"class": "tests.test_utils.Bar", "params": {"b": 20, "c": 30}},
            Bar(10, 20, 30, 40),
        ),
        (
            {"class": "tests.test_utils.Bar", "params": {"b": 200, "c": "${params.b}"}},
            Bar(10, 200, 200, 40),
        ),
    ],
)
def test_class_instantiate_passthrough(conf, expected):
    conf = OmegaConf.create(conf)
    obj = utils.instantiate(conf, 10, d=40)
    assert obj == expected
