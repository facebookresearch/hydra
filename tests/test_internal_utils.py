# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any

import pytest
from _pytest.python_api import RaisesContext
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
        pytest.param(
            OmegaConf.create({"_target_": "foo"}), "foo", False, id="ObjectConf:target"
        ),
        pytest.param(
            OmegaConf.create({"cls": "foo"}), "foo", "cls", id="DictConfig:cls"
        ),
        pytest.param(
            OmegaConf.create({"class": "foo"}), "foo", "class", id="DictConfig:class"
        ),
        pytest.param(
            OmegaConf.create({"target": "foo"}),
            "foo",
            "target",
            id="DictConfig:target",
        ),
        pytest.param(
            OmegaConf.create({"cls": "foo", "_target_": "bar"}),
            "bar",
            False,
            id="DictConfig:cls_target",
        ),
        pytest.param(
            OmegaConf.create({"class": "foo", "_target_": "bar"}),
            "bar",
            "class",
            id="DictConfig:class_target",
        ),
        # check that `target` is prioritized over `cls`/`class`.
        pytest.param(
            OmegaConf.create({"cls": "foo", "_target_": "bar"}),
            "bar",
            "cls",
            id="DictConfig:pri_cls",
        ),
        pytest.param(
            OmegaConf.create({"class": "foo", "_target_": "bar"}),
            "bar",
            "class",
            id="DictConfig:pri_class",
        ),
        pytest.param(
            OmegaConf.create({"target": "foo", "_target_": "bar"}),
            "bar",
            "target",
            id="DictConfig:pri_target",
        ),
    ],
)
def test_get_class_name(
    config: DictConfig, expected: Any, warning: Any, recwarn: Any
) -> None:
    assert utils._get_cls_name(config) == expected

    target_field_deprecated = (
        "\nConfig key '{key}' is deprecated since Hydra 1.0 and will be removed in Hydra 1.1."
        "\nUse '_target_' instead of '{field}'."
        "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
    )

    if warning is not False:
        assert recwarn[0].category == UserWarning
        assert recwarn[0].message.args[0] == target_field_deprecated.format(
            key=warning, field=warning
        )


# TODO: why?
# @pytest.mark.skipif(  # type: ignore
#     sys.version_info < (3, 7), reason="requires python3.7"
# )
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


def test_object_conf_deprecated() -> None:
    msg = (
        "\nObjectConf is deprecated in favor of TargetConf since Hydra 1.0.0rc3 and will be removed in Hydra 1.1."
        "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/object_instantiation_changes"
    )

    with pytest.warns(expected_warning=UserWarning, match=msg):
        ObjectConf(target="foo")
