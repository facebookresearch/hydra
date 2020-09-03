# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from pathlib import Path
from typing import Any

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root, get_run_output, run_with_error

chdir_hydra_root()


def test_1_basic_run(tmpdir: Path) -> None:
    result, _err = get_run_output(
        [
            "examples/tutorials/structured_configs/1_minimal/my_app.py",
            "hydra.run.dir=" + str(tmpdir),
        ]
    )
    assert result == "Host: localhost, port: 3306"


def test_1_basic_run_with_override_error(tmpdir: Path) -> None:
    expected = """Key 'pork' not in 'MySQLConfig'
\tfull_key: pork
\treference_type=Optional[MySQLConfig]
\tobject_type=MySQLConfig"""
    err = run_with_error(
        [
            "examples/tutorials/structured_configs/1_minimal/my_app_type_error.py",
            "hydra.run.dir=" + str(tmpdir),
        ]
    )
    assert re.search(re.escape(expected), err) is not None


def test_1_basic_override(tmpdir: Path) -> None:
    result, _err = get_run_output(
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

    expected = """Value 'foo' could not be converted to Integer
\tfull_key: port
\treference_type=Optional[MySQLConfig]
\tobject_type=MySQLConfig"""

    err = run_with_error(cmd)
    assert re.search(re.escape(expected), err) is not None


def test_2_static_complex(tmpdir: Path) -> None:
    result, _err = get_run_output(
        [
            "examples/tutorials/structured_configs/2_static_complex/my_app.py",
            "hydra.run.dir=" + str(tmpdir),
        ]
    )
    assert result == "Title=My app, size=1024x768 pixels"


@pytest.mark.parametrize(  # type: ignore
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
    result, _err = get_run_output(cmd)
    res = OmegaConf.create(result)
    assert res == expected


@pytest.mark.parametrize(  # type: ignore
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
    result, _err = get_run_output(cmd)
    res = OmegaConf.create(result)
    assert res == expected


def test_4_defaults(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/structured_configs/4_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }


def test_5_structured_config_schema(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/structured_configs/5_structured_config_schema/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }


def test_6_one_schema_many_configs(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/structured_configs/6_static_schema_many_configs/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        "db=prod",
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == {
        "db": {
            "driver": "mysql",
            "host": "mysql001.prod",
            "user": "root",
            "password": "1234",
        }
    }


def test_7_multiple_schemas_multiple_configs(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/structured_configs/7_dynamic_schema_many_configs/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == {
        "db": {"driver": "mysql", "host": "mysql001.staging", "encoding": "utf-8"}
    }
