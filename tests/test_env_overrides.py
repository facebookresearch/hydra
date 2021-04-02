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
            "tests/test_apps/app_with_env_overrides/my_app.py",
            [],
            dedent(
                """\
                [JOB] DefaultCallback on_job_start
                foo: bar

                [JOB] DefaultCallback on_job_end"""
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
