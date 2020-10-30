# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from textwrap import dedent
from typing import Any

from hydra.test_utils.test_utils import (
    TTaskRunner,
    assert_text_same,
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

    expected = dedent(
        """\
        Error merging override data_bits=10
        Cannot change read-only config container
        \tfull_key: data_bits
        \treference_type=Optional[SerialPort]
        \tobject_type=SerialPort

        Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
        """
    )
    err = run_with_error(cmd)
    assert_text_same(from_line=expected, to_line=err)
