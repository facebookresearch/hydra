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
    "app_path,args,expected",
    [
        (
            "tests/test_apps/app_with_callbacks/custom_callback/my_app.py",
            [],
            dedent(
                """\
                [HYDRA] Init CustomCallback with self.param1=value1, self.param2=value2
                [HYDRA] CustomCallback on_run_start
                [JOB] CustomCallback on_job_start
                foo: bar

                [JOB] CustomCallback on_job_end
                [JOB] CustomCallback on_run_end"""
            ),
        ),
        (
            "tests/test_apps/app_with_callbacks/custom_callback/my_app.py",
            [
                "foo=bar",
                "-m",
            ],
            dedent(
                """\
                [HYDRA] Init CustomCallback with self.param1=value1, self.param2=value2
                [HYDRA] CustomCallback on_multirun_start
                [HYDRA] Launching 1 jobs locally
                [HYDRA] \t#0 : foo=bar
                [JOB] CustomCallback on_job_start
                foo: bar

                [JOB] CustomCallback on_job_end
                [HYDRA] CustomCallback on_multirun_end"""
            ),
        ),
        (
            "tests/test_apps/app_with_callbacks/default_callback/my_app.py",
            [],
            dedent(
                """\
                [HYDRA] Init DefaultCallback with self.param1=foo, self.param2=bar
                [HYDRA] DefaultCallback on_run_start
                [JOB] DefaultCallback on_job_start
                foo: bar

                [JOB] DefaultCallback on_job_end
                [JOB] DefaultCallback on_run_end"""
            ),
        ),
        (
            "tests/test_apps/app_with_callbacks/default_callback/my_app.py",
            [
                "hydra/callbacks=[custom_callback]",
            ],
            dedent(
                """\
                [HYDRA] Init CustomCallback with self.param1=value1, self.param2=value2
                [HYDRA] Init DefaultCallback with self.param1=foo, self.param2=bar
                [HYDRA] CustomCallback on_run_start
                [HYDRA] DefaultCallback on_run_start
                [JOB] CustomCallback on_job_start
                [JOB] DefaultCallback on_job_start
                foo: bar

                [JOB] CustomCallback on_job_end
                [JOB] DefaultCallback on_job_end
                [JOB] CustomCallback on_run_end
                [JOB] DefaultCallback on_run_end"""
            ),
        ),
        (
            "tests/test_apps/app_with_callbacks/default_callback/my_app.py",
            [
                "foo=bar",
                "-m",
            ],
            dedent(
                """\
                    [HYDRA] Init DefaultCallback with self.param1=foo, self.param2=bar
                    [HYDRA] DefaultCallback on_multirun_start
                    [HYDRA] Launching 1 jobs locally
                    [HYDRA] \t#0 : foo=bar
                    [JOB] DefaultCallback on_job_start
                    foo: bar

                    [JOB] DefaultCallback on_job_end
                    [HYDRA] DefaultCallback on_multirun_end"""
            ),
        ),
        (
            "tests/test_apps/app_with_callbacks/default_callback/my_app.py",
            [
                "hydra/callbacks=[custom_callback]",
                "foo=bar",
                "-m",
            ],
            dedent(
                """\
                    [HYDRA] Init CustomCallback with self.param1=value1, self.param2=value2
                    [HYDRA] Init DefaultCallback with self.param1=foo, self.param2=bar
                    [HYDRA] CustomCallback on_multirun_start
                    [HYDRA] DefaultCallback on_multirun_start
                    [HYDRA] Launching 1 jobs locally
                    [HYDRA] \t#0 : foo=bar
                    [JOB] CustomCallback on_job_start
                    [JOB] DefaultCallback on_job_start
                    foo: bar

                    [JOB] CustomCallback on_job_end
                    [JOB] DefaultCallback on_job_end
                    [HYDRA] CustomCallback on_multirun_end
                    [HYDRA] DefaultCallback on_multirun_end"""
            ),
        ),
    ],
)
def test_app_with_callbacks(
    tmpdir: Path,
    app_path: str,
    args: List[str],
    expected: str,
) -> None:

    cmd = [
        app_path,
        "hydra.run.dir=" + str(tmpdir),
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
