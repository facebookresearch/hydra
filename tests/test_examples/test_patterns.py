# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import sys
from pathlib import Path
from subprocess import check_output
from typing import Any, List

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra.test_utils.test_utils import (
    TTaskRunner,
    chdir_hydra_root,
    verify_dir_outputs,
)
from tests.test_examples import run_with_error

chdir_hydra_root()


# TODO: fails in pip install mode, need to figure out a solution for tests that needs to install modules.
# A reasonable solution is to only test the examples in the directory with pip install -e through nox.
@pytest.mark.skip("Disabled")  # type: ignore
def test_patterns_objects(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/patterns/objects/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = check_output(cmd)
    assert (
        result.decode("utf-8").rstrip()
        == "MySQL connecting to localhost with user=root and password=1234"
    )


def test_specializing_config_example(
    hydra_restore_singletons: Any, hydra_task_runner: TTaskRunner
) -> None:
    with hydra_task_runner(
        calling_file="examples/patterns/specializing_config/example.py",
        calling_module=None,
        config_path="conf",
        config_name="config.yaml",
        overrides=["dataset=cifar10"],
    ) as task:
        assert task.job_ret is not None and task.job_ret.cfg == dict(
            dataset=dict(name="cifar10", path="/datasets/cifar10"),
            model=dict(num_layers=5, type="alexnet"),
        )
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


@pytest.mark.parametrize(  # type: ignore
    "args,output_conf",
    [
        (
            [],
            {
                "db": {
                    "target": "examples.patterns.instantiate.objects.my_app.MySQLConnection",
                    "params": {"host": "localhost", "user": "root", "password": 1234},
                }
            },
        ),
        (
            ["db=postgresql"],
            {
                "db": {
                    "target": "examples.patterns.instantiate.objects.my_app.PostgreSQLConnection",
                    "params": {
                        "host": "localhost",
                        "user": "root",
                        "password": 1234,
                        "database": "tutorial",
                    },
                }
            },
        ),
    ],
)
def test_instantiate_objects_example(
    hydra_restore_singletons: Any,
    tmpdir: Path,
    hydra_task_runner: TTaskRunner,
    args: List[str],
    output_conf: DictConfig,
) -> None:
    with hydra_task_runner(
        calling_file="examples/patterns/instantiate/objects/my_app.py",
        calling_module=None,
        config_path="conf",
        config_name="config.yaml",
        overrides=args,
    ) as task:
        assert task.job_ret is not None
        assert task.job_ret.cfg == output_conf
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


@pytest.mark.parametrize(  # type: ignore
    "overrides,output",
    [
        ([], "MySQL connecting to localhost with user=root and password=1234"),
        (
            ["db=postgresql"],
            "PostgreSQL connecting to localhost with user=root and password=1234 and database=tutorial",
        ),
    ],
)
def test_instantiate_structured_config_example(
    tmpdir: Path, overrides: List[str], output: str,
) -> None:

    cmd = [
        sys.executable,
        "examples/patterns/instantiate/structured_config/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ] + overrides
    result = check_output(cmd)
    assert result.decode("utf-8").rstrip() == output


def test_frozen(tmpdir: Any) -> None:
    cmd = [
        sys.executable,
        "examples/patterns/write_protect_config_node/frozen.py",
        "hydra.run.dir=" + str(tmpdir),
        "data_bits=10",
    ]

    err = run_with_error(cmd)
    assert re.search(re.escape("Error merging override data_bits=10"), err) is not None
