# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from textwrap import dedent
from typing import List

from pytest import mark

from hydra.test_utils.test_utils import (
    assert_regex_match,
    chdir_hydra_root,
    run_python_script,
)

chdir_hydra_root()


@mark.parametrize(
    "args,expected",
    [
        (
            [],
            dedent(
                """\
                [HYDRA] Init custom_callback
                [HYDRA] custom_callback on_run_start
                [JOB] custom_callback on_job_start
                [JOB] foo: bar

                [JOB] custom_callback on_job_end
                [JOB] custom_callback on_run_end"""
            ),
        ),
        (
            [
                "foo=bar",
                "-m",
            ],
            dedent(
                """\
                [HYDRA] Init custom_callback
                [HYDRA] custom_callback on_multirun_start
                [HYDRA] Launching 1 jobs locally
                [HYDRA] \t#0 : foo=bar
                [JOB] custom_callback on_job_start
                [JOB] foo: bar

                [JOB] custom_callback on_job_end
                [HYDRA] custom_callback on_multirun_end"""
            ),
        ),
        (
            [
                "--config-name",
                "config_with_two_callbacks",
            ],
            dedent(
                """\
                [HYDRA] Init callback_1
                [HYDRA] Init callback_2
                [HYDRA] callback_1 on_run_start
                [HYDRA] callback_2 on_run_start
                [JOB] callback_1 on_job_start
                [JOB] callback_2 on_job_start
                [JOB] {}

                [JOB] callback_2 on_job_end
                [JOB] callback_1 on_job_end
                [JOB] callback_2 on_run_end
                [JOB] callback_1 on_run_end"""
            ),
        ),
    ],
)
def test_app_with_callbacks(
    tmpdir: Path,
    args: List[str],
    expected: str,
) -> None:
    app_path = "tests/test_apps/app_with_callbacks/custom_callback/my_app.py"

    cmd = [
        app_path,
        "hydra.run.dir=" + str(tmpdir),
        "hydra.job.chdir=True",
        "hydra.hydra_logging.formatters.simple.format='[HYDRA] %(message)s'",
        "hydra.job_logging.formatters.simple.format='[JOB] %(message)s'",
    ]
    cmd.extend(args)
    result, _err = run_python_script(cmd)

    assert_regex_match(
        from_line=expected,
        to_line=result,
        from_name="Expected output",
        to_name="Actual output",
    )
