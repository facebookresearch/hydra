# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import sys
from pathlib import Path
from subprocess import check_output
from typing import Any

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root

from . import run_with_error

chdir_hydra_root()


def test_structured_configs_1_basic_run(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/1_minimal/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = check_output(cmd)
    assert result.decode("utf-8").rstrip() == "Host: localhost, port: 3306"


def test_structured_configs_1_basic_run_with_override_error(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/1_minimal/my_app_type_error.py",
        "hydra.run.dir=" + str(tmpdir),
    ]

    expected = """Key 'pork' not in 'MySQLConfig'
\tfull_key: pork
\treference_type=Optional[MySQLConfig]
\tobject_type=MySQLConfig"""
    err = run_with_error(cmd)
    assert re.search(re.escape(expected), err) is not None


def test_structured_configs_1_basic_override(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/1_minimal/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        "port=9090",
    ]
    result = check_output(cmd)
    assert result.decode("utf-8").rstrip() == "Host: localhost, port: 9090"


def test_structured_configs_1_basic_override_type_error(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
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


def test_structured_configs_2_nesting_configs__with_dataclass(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/2_nesting_configs/nesting_with_dataclass.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = check_output(cmd)
    assert result.decode().rstrip() == "Host: localhost, port: 3306"


def test_structured_configs_2_nesting_configs__with_ad_hoc_node(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/2_nesting_configs/nesting_with_ad_hoc_node.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = check_output(cmd)
    assert result.decode().rstrip() == "Copying localhost:3306 to example.com:3306"


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
def test_structured_configs_3_config_groups(
    tmpdir: Path, overrides: Any, expected: Any
) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/3_config_groups/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(overrides)
    result = check_output(cmd)
    res = OmegaConf.create(result.decode().rstrip())
    assert res == expected


def test_structured_configs_3_config_groups_with_inheritance(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/3_config_groups/my_app_with_inheritance.py",
        "hydra.run.dir=" + str(tmpdir),
        "+db=mysql",
    ]
    result = check_output(cmd)
    assert result.decode().rstrip() == "Connecting to MySQL: localhost:3306"


def test_structured_configs_4_defaults(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/4_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = check_output(cmd)
    assert OmegaConf.create(result.decode("utf-8").rstrip()) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }


def test_structured_configs_5_structured_config_schema(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/structured_configs/5_structured_config_schema/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = check_output(cmd)
    assert OmegaConf.create(result.decode("utf-8").rstrip()) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }
