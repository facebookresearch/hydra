# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from pathlib import Path

import pytest
from omegaconf import OmegaConf

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import (  # noqa: F401
    TSweepRunner,
    TTaskRunner,
    chdir_hydra_root,
    does_not_raise,
    sweep_runner,
    task_runner,
    verify_dir_outputs,
)

chdir_hydra_root()


def test_structured_configs_1_basic_run(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/structured_configs_tutorial/1_basic/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert (
        result.decode("utf-8").rstrip()
        == "Connecting to mysql at localhost:3306, user=omry, password=secret"
    )


def test_structured_configs_1_basic_override(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/structured_configs_tutorial/1_basic/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        "port=9090",
    ]
    result = subprocess.check_output(cmd)
    assert (
        result.decode("utf-8").rstrip()
        == "Connecting to mysql at localhost:9090, user=omry, password=secret"
    )


def test_structured_configs_1_basic_override_type_error(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/structured_configs_tutorial/1_basic/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        "port=foo",
    ]
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output(cmd)


def test_structured_configs_2_node_path(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/structured_configs_tutorial/2_node_path/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert (
        result.decode("utf-8").rstrip()
        == "Connecting to mysql at localhost:3306, user=omry, password=secret"
    )


@pytest.mark.parametrize(  # type: ignore
    "file",
    [
        "examples/structured_configs_tutorial/2_node_path/my_app.py",
        "examples/structured_configs_tutorial/3_nesting_configs/my_app.py",
    ],
)
def test_structured_configs_2_and_3_override(tmpdir: Path, file: str) -> None:
    cmd = [
        sys.executable,
        file,
        "hydra.run.dir=" + str(tmpdir),
        "db.port=9090",
    ]
    result = subprocess.check_output(cmd)
    assert (
        result.decode("utf-8").rstrip()
        == "Connecting to mysql at localhost:9090, user=omry, password=secret"
    )


@pytest.mark.parametrize(  # type: ignore
    "file",
    [
        "examples/structured_configs_tutorial/4_config_groups/my_app.py",
        "examples/structured_configs_tutorial/4_config_groups/my_app_with_inheritance.py",
    ],
)
def test_structured_configs_4_config_groups(tmpdir: Path, file: str) -> None:
    result = subprocess.check_output(
        [sys.executable, file, "hydra.run.dir=" + str(tmpdir)]
    )
    assert OmegaConf.create(result.decode("utf-8").rstrip()) == {"db": "???"}

    result = subprocess.check_output(
        [sys.executable, file, "hydra.run.dir=" + str(tmpdir), "db=mysql"]
    )
    assert OmegaConf.create(result.decode("utf-8").rstrip()) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }


def test_structured_configs_5_defaults(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/structured_configs_tutorial/5_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(result.decode("utf-8").rstrip()) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }


def test_structured_configs_6_structured_config_schema(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/structured_configs_tutorial/6_structured_config_schema/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(result.decode("utf-8").rstrip()) == {
        "db": {
            "driver": "mysql",
            "host": "localhost",
            "password": "secret",
            "port": 3306,
            "user": "omry",
        }
    }
