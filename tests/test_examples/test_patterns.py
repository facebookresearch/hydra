# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any

from hydra.test_utils.test_utils import (
    TTaskRunner,
    chdir_hydra_root,
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


def test_write_protect_config_node(tmpdir: Any) -> None:
    cmd = [
        "examples/patterns/write_protect_config_node/frozen.py",
        "hydra.run.dir=" + str(tmpdir),
        "data_bits=10",
    ]

    err = run_with_error(cmd)
    assert re.search(re.escape("Error merging override data_bits=10"), err) is not None
