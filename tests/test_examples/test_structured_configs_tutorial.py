# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import (
    chdir_hydra_root,
    run_python_script,
    run_with_error,
)

chdir_hydra_root()


def test_1_basic_run(tmpdir: Path) -> None:
    result, _err = run_python_script(
        [
            "examples/tutorials/structured_configs/1_minimal/my_app.py",
            "hydra.run.dir=" + str(tmpdir),
        ]
    )
    assert result == "Host: localhost, port: 3306"


def test_1_basic_run_with_override_error(tmpdir: Path) -> None:
    expected = dedent(
        """\
        Key 'pork' not in 'MySQLConfig'
            full_key: pork
            object_type=MySQLConfig"""
    )
    err = run_with_error(
        [
            "examples/tutorials/structured_configs/1_minimal/my_app_type_error.py",
            "hydra.run.dir=" + str(tmpdir),
        ]
    )
    assert re.search(re.escape(expected), err) is not None


def test_1_basic_override(tmpdir: Path) -> None:
    result, _err = run_python_script(
        [
            "examples/tutorials/structured_configs/1_minimal/my_app.py",
            "hydra.run.dir=" + str(tmpdir),
            "port=9090",
        ]
    )
    assert result == "Host: localhost, port: 9090"


def test_1_basic_override_type_error(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/structured_configs/1_minimal/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        "port=foo",
    ]

    expected = dedent(
        """\
        Value 'foo' could not be converted to Integer
            full_key: port
            object_type=MySQLConfig"""
    )

    err = run_with_error(cmd)
    assert re.search(re.escape(expected), err) is not None


def test_2_static_complex(tmpdir: Path) -> None:
    result, _err = run_python_script(
        [
            "examples/tutorials/structured_configs/2_static_complex/my_app.py",
            "hydra.run.dir=" + str(tmpdir),
        ]
    )
    assert result == "Title=My app, size=1024x768 pixels"


@pytest.mark.parametrize(
    "overrides,expected",
    [
        ([], {"db": "???"}),
        (
            ["+db=mysql"],
            {"db": {"driver": "mysql", "host": "localhost", "port": 3306}},
        ),
    ],
)
def test_3_config_groups(tmpdir: Path, overrides: Any, expected: Any) -> None:
    cmd = [
        "examples/tutorials/structured_configs/3_config_groups/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(overrides)
    result, _err = run_python_script(cmd)
    res = OmegaConf.create(result)
    assert res == expected


@pytest.mark.parametrize(
    "overrides,expected",
    [
        ([], {"db": "???"}),
        (
            ["+db=mysql"],
            {"db": {"driver": "mysql", "host": "localhost", "port": 3306}},
        ),
        (
            ["+db=postgresql"],
            {
                "db": {
                    "driver": "postgresql",
                    "host": "localhost",
                    "port": 5432,
                    "timeout": 10,
                }
            },
        ),
    ],
)
def test_3_config_groups_with_inheritance(
    tmpdir: Path, overrides: Any, expected: Any
) -> None:
    cmd = [
        "examples/tutorials/structured_configs/3_config_groups/my_app_with_inheritance.py",
        "hydra.run.dir=" + str(tmpdir),
    ] + overrides
    result, _err = run_python_script(cmd)
    res = OmegaConf.create(result)
    assert res == expected


def test_4_defaults(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/structured_configs/4_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = run_python_script(cmd)
    assert OmegaConf.create(result) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }


@pytest.mark.parametrize(
    "path",
    [
        "examples/tutorials/structured_configs/5.1_structured_config_schema_same_config_group/my_app.py",
        "examples/tutorials/structured_configs/5.2_structured_config_schema_different_config_group/my_app.py",
    ],
)
def test_5_structured_config_schema(tmpdir: Path, path: str) -> None:
    cmd = [path, "hydra.run.dir=" + str(tmpdir)]
    result, _err = run_python_script(cmd)
    assert OmegaConf.create(result) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        },
        "debug": True,
    }
