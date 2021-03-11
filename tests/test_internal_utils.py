# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from omegaconf import DictConfig, OmegaConf
from pytest import mark, param

from hydra._internal import utils


@mark.parametrize(
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


@mark.parametrize(
    "config, expected",
    [
        param(OmegaConf.create({"_target_": "foo"}), "foo", id="ObjectConf:target"),
    ],
)
def test_get_class_name(config: DictConfig, expected: Any) -> None:
    assert utils._get_cls_name(config) == expected
