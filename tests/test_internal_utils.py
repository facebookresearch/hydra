# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Callable, Optional

from omegaconf import DictConfig, OmegaConf
from pytest import mark, param

from hydra._internal import utils
from tests import data


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


@mark.parametrize(
    "task_function, expected_file, expected_module",
    [
        param(data.foo, None, "tests.data", id="function"),
        param(data.foo_main_module, data.__file__, None, id="function-main-module"),
        param(data.Bar, None, "tests.data", id="class"),
        param(data.bar_instance, None, "tests.data", id="class_inst"),
        param(data.bar_instance_main_module, None, None, id="class_inst-main-module"),
    ],
)
def test_detect_calling_file_or_module_from_task_function(
    task_function: Callable[..., None],
    expected_file: Optional[str],
    expected_module: Optional[str],
) -> None:
    file, module = utils.detect_calling_file_or_module_from_task_function(task_function)
    assert file == expected_file
    assert module == expected_module
