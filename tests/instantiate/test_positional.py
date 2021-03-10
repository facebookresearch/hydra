from typing import Any

from hydra.utils import instantiate
from pytest import mark, param


class ArgsClass:
    def __init__(self, *args, **kwargs):
        assert isinstance(args, tuple)
        assert isinstance(kwargs, dict)
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return f"{self.args=},{self.kwargs=}"

    def __eq__(self, other):
        if isinstance(other, ArgsClass):
            return self.args == other.args and self.kwargs == other.kwargs
        else:
            return NotImplemented


#######################
# non-recursive tests #
#######################


@mark.parametrize(
    ("cfg", "expected"),
    [
        param(
            {"_target_": "tests.test_instantiate.ArgsClass"},
            ArgsClass(),
            id="config:no_params",
        ),
        param(
            {"_target_": "tests.test_instantiate.ArgsClass", "_args_": [1]},
            ArgsClass(1),
            id="config:args_only",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "_args_": [1],
                "foo": 10,
            },
            ArgsClass(1, foo=10),
            id="config:args+kwargs",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "foo": 10,
            },
            ArgsClass(foo=10),
            id="config:kwargs_only",
        ),
    ],
)
def test_instantiate_args_kwargs(cfg: Any, expected: Any) -> None:
    assert instantiate(cfg) == expected


@mark.parametrize(
    ("cfg", "expected"),
    [
        param(
            {"_target_": "tests.test_instantiate.ArgsClass", "_args_": ["${.1}", 2]},
            ArgsClass(2, 2),
            id="config:args_only",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "_args_": [1],
                "foo": "${._args_}",
            },
            ArgsClass(1, foo=[1]),
            id="config:args+kwargs",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "foo": "${._target_}",
            },
            ArgsClass(foo="tests.test_instantiate.ArgsClass"),
            id="config:kwargs_only)",
        ),
    ],
)
def test_instantiate_args_kwargs_with_interpolation(cfg: Any, expected: Any) -> None:
    assert instantiate(cfg) == expected


@mark.parametrize(
    ("cfg", "args_override", "kwargs_override", "expected"),
    [
        param(
            {"_target_": "tests.test_instantiate.ArgsClass", "_args_": [1]},
            [2],
            {},
            ArgsClass(2),
            id="direct_args",
        ),
        param(
            {"_target_": "tests.test_instantiate.ArgsClass", "_args_": [1]},
            [],
            {"_args_": [2]},
            ArgsClass(2),
            id="indirect_args",
        ),
        param(
            {"_target_": "tests.test_instantiate.ArgsClass", "_args_": [1]},
            [],
            {"foo": 10},
            ArgsClass(1, foo=10),
            id="kwargs",
        ),
        param(
            {"_target_": "tests.test_instantiate.ArgsClass", "_args_": [1]},
            [],
            {"foo": 10, "_args_": [2]},
            ArgsClass(2, foo=10),
            id="kwargs+indirect_args",
        ),
    ],
)
def test_instantiate_args_kwargs_with_override(
    cfg: Any, args_override: Any, expected: Any, kwargs_override: Any
) -> None:
    assert instantiate(cfg, *args_override, **kwargs_override) == expected


# TODO: recursive

###################
# recursive tests #
###################


@mark.parametrize(
    ("cfg", "expected"),
    [
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "child": {"_target_": "tests.test_instantiate.ArgsClass"},
            },
            ArgsClass(child=ArgsClass()),
            id="config:no_params",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "_args_": [1],
                "child": {
                    "_target_": "tests.test_instantiate.ArgsClass",
                    "_args_": [2],
                },
            },
            ArgsClass(1, child=ArgsClass(2)),
            id="config:args_only",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "_args_": [1],
                "foo": 10,
                "child": {
                    "_target_": "tests.test_instantiate.ArgsClass",
                    "_args_": [2],
                },
            },
            ArgsClass(1, foo=10, child=ArgsClass(2)),
            id="config:args+kwargs",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "child": {
                    "_target_": "tests.test_instantiate.ArgsClass",
                    "_args_": [2],
                },
                "foo": 10,
            },
            ArgsClass(foo=10, child=ArgsClass(2)),
            id="config:kwargs_only",
        ),
    ],
)
def test_recursive_instantiate_args_kwargs(cfg: Any, expected: Any) -> None:
    assert instantiate(cfg) == expected


@mark.parametrize(
    ("cfg", "args_override", "kwargs_override", "expected"),
    [
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "child": {"_target_": "tests.test_instantiate.ArgsClass"},
            },
            [1],
            {},
            ArgsClass(1, child=ArgsClass()),
            id="direct_args_not_in_nested",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "_args_": [1],
                "child": {
                    "_target_": "tests.test_instantiate.ArgsClass",
                    "_args_": [2],
                },
            },
            [],
            {"_args_": [3], "child": {"_args_": [4]}},
            ArgsClass(3, child=ArgsClass(4)),
            id="indirect_args",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "_args_": [1],
                "child": {
                    "_target_": "tests.test_instantiate.ArgsClass",
                    "_args_": [2],
                },
            },
            [],
            {"foo": 10},
            ArgsClass(1, foo=10, child=ArgsClass(2)),
            id="kwargs",
        ),
        param(
            {
                "_target_": "tests.test_instantiate.ArgsClass",
                "_args_": [1],
                "child": {
                    "_target_": "tests.test_instantiate.ArgsClass",
                    "_args_": [2],
                },
            },
            [],
            {"foo": 10, "_args_": [3], "child": {"_args_": [4]}},
            ArgsClass(3, foo=10, child=ArgsClass(4)),
            id="kwargs+indirect_args",
        ),
    ],
)
def test_recursive_instantiate_args_kwargs_with_override(
    cfg: Any, args_override: Any, expected: Any, kwargs_override: Any
) -> None:
    assert instantiate(cfg, *args_override, **kwargs_override) == expected
