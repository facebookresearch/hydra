import pytest
from hydra import utils


def some_method():
    return 42


class Foo:
    @staticmethod
    def static_method():
        return 43


@pytest.mark.parametrize('path,expected_type', [
    ('tests.test_utils.Foo', Foo),
])
def test_get_class(path, expected_type):
    assert utils.get_class(path) == expected_type


@pytest.mark.parametrize('path,return_value', [
    ('tests.test_utils.some_method', 42),
])
def test_get_method(path, return_value):
    assert utils.get_method(path)() == return_value


@pytest.mark.parametrize('path,return_value', [
    ('tests.test_utils.Foo.static_method', 43),
])
def test_get_static_method(path, return_value):
    assert utils.get_static_method(path)() == return_value
