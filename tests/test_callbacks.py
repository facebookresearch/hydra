# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import pickle
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any, List

from omegaconf import open_dict, read_write
from pytest import mark

from hydra.core.utils import JobReturn, JobStatus
from hydra.test_utils.test_utils import (
    assert_regex_match,
    chdir_hydra_root,
    run_process,
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


@mark.parametrize("multirun", [True, False])
def test_experimental_save_job_info_callback(tmpdir: Path, multirun: bool) -> None:
    app_path = "tests/test_apps/app_with_pickle_job_info_callback/my_app.py"

    cmd = [
        app_path,
        "hydra.run.dir=" + str(tmpdir),
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra.job.chdir=True",
    ]
    if multirun:
        cmd.append("-m")
    _, _err = run_python_script(cmd)

    def load_pickle(path: Path) -> Any:
        with open(str(path), "rb") as input:
            obj = pickle.load(input)  # nosec
        return obj

    # load pickles from callbacks
    callback_output = tmpdir / Path("0") / ".hydra" if multirun else tmpdir / ".hydra"
    config_on_job_start = load_pickle(callback_output / "config.pickle")
    job_return_on_job_end: JobReturn = load_pickle(
        callback_output / "job_return.pickle"
    )

    task_cfg_from_callback = copy.deepcopy(config_on_job_start)
    with read_write(task_cfg_from_callback):
        with open_dict(task_cfg_from_callback):
            del task_cfg_from_callback["hydra"]

    # load pickles generated from the application
    app_output_dir = tmpdir / "0" if multirun else tmpdir
    task_cfg_from_app = load_pickle(app_output_dir / "task_cfg.pickle")
    hydra_cfg_from_app = load_pickle(app_output_dir / "hydra_cfg.pickle")

    # verify the cfg pickles are the same on_job_start
    assert task_cfg_from_callback == task_cfg_from_app
    assert config_on_job_start.hydra == hydra_cfg_from_app

    # verify pickled object are the same on_job_end
    assert job_return_on_job_end.cfg == task_cfg_from_app
    assert job_return_on_job_end.hydra_cfg.hydra == hydra_cfg_from_app  # type: ignore
    assert job_return_on_job_end.return_value == "hello world"
    assert job_return_on_job_end.status == JobStatus.COMPLETED


@mark.parametrize("multirun", [True, False])
def test_save_job_return_callback(tmpdir: Path, multirun: bool) -> None:
    app_path = "tests/test_apps/app_with_log_jobreturn_callback/my_app.py"
    cmd = [
        sys.executable,
        app_path,
        "hydra.run.dir=" + str(tmpdir),
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra.job.chdir=True",
    ]
    if multirun:
        extra = ["+x=0,1", "-m"]
        cmd.extend(extra)
    log_msg = "omegaconf.errors.ConfigAttributeError: Key 'divisor' is not in struct\n"
    run_process(cmd=cmd, print_error=False, raise_exception=False)

    if multirun:
        log_paths = [tmpdir / "0" / "my_app.log", tmpdir / "1" / "my_app.log"]
    else:
        log_paths = [tmpdir / "my_app.log"]

    for p in log_paths:
        with open(p, "r") as file:
            logs = file.readlines()
            assert log_msg in logs
