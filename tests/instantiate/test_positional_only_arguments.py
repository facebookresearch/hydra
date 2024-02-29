# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from pytest import mark, param

from hydra.utils import instantiate

from .positional_only import PosOnlyArgsClass


@mark.parametrize(
    ("cfg", "args", "expected"),
    [
        param(
            {
                "_target_": "tests.instantiate.positional_only.PosOnlyArgsClass",
                "_args_": [1, 2],
            },
            [],
            PosOnlyArgsClass(1, 2),
            id="pos_only_in_config",
        ),
        param(
            {
                "_target_": "tests.instantiate.positional_only.PosOnlyArgsClass",
            },
            [1, 2],
            PosOnlyArgsClass(1, 2),
            id="pos_only_in_override",
        ),
        param(
            {
                "_target_": "tests.instantiate.positional_only.PosOnlyArgsClass",
                "_args_": [1, 2],
            },
            [3, 4],
            PosOnlyArgsClass(3, 4),
            id="pos_only_in_both",
        ),
    ],
)
def test_positional_only_arguments(cfg: Any, args: Any, expected: Any) -> None:
    assert instantiate(cfg, *args) == expected
