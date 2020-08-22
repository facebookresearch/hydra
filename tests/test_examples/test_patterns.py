# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from pathlib import Path
from typing import Any, List

import pytest

from hydra.test_utils.test_utils import (
    TTaskRunner,
    chdir_hydra_root,
    get_run_output,
    run_with_error,
    verify_dir_outputs,
)

chdir_hydra_root()


def test_specializing_config_example(
    hydra_restore_singletons: Any, hydra_task_runner: TTaskRunner
) -> None:
    with hydra_task_runner(
        calling_file="examples/patterns/specializing_config/example.py",
        calling_module=None,
        config_path="conf",
        config_name="config.yaml",
        overrides=["dataset=cifar10"],
        configure_logging=True,
    ) as task:
        assert task.job_ret is not None and task.job_ret.cfg == dict(
            dataset=dict(name="cifar10", path="/datasets/cifar10"),
            model=dict(num_layers=5, type="alexnet"),
        )
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


@pytest.mark.parametrize(  # type: ignore
    "overrides,output",
    [
        ([], "MySQL connecting to localhost"),
        (["db=postgresql"], "PostgreSQL connecting to localhost",),
    ],
)
def test_instantiate_objects_example(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], output: str,
) -> None:
    monkeypatch.chdir("examples/patterns/instantiate/objects/")
    cmd = ["my_app.py", "hydra.run.dir=" + str(tmpdir)] + overrides
    result = get_run_output(cmd)
    assert result == output


@pytest.mark.parametrize(  # type: ignore
    "overrides,output",
    [
        ([], "MySQL connecting to localhost"),
        (["db=postgresql"], "PostgreSQL connecting to localhost",),
    ],
)
def test_instantiate_structured_config_example(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], output: str,
) -> None:
    monkeypatch.chdir("examples/patterns/instantiate/structured_config/")
    cmd = ["my_app.py", "hydra.run.dir=" + str(tmpdir)] + overrides
    result = get_run_output(cmd)
    assert result == output


def test_frozen(tmpdir: Any) -> None:
    cmd = [
        "examples/patterns/write_protect_config_node/frozen.py",
        "hydra.run.dir=" + str(tmpdir),
        "data_bits=10",
    ]

    err = run_with_error(cmd)
    assert re.search(re.escape("Error merging override data_bits=10"), err) is not None
