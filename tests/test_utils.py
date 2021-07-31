# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import io
import os
from pathlib import Path
from textwrap import dedent
from typing import Any
from unittest.mock import patch

from omegaconf import DictConfig, OmegaConf
from pytest import mark, raises

from hydra import utils
from hydra._internal.utils import run_and_report
from hydra.conf import HydraConf, RuntimeConf
from hydra.core.hydra_config import HydraConfig
from hydra.test_utils.test_utils import assert_regex_match


def test_get_original_cwd(hydra_restore_singletons: Any) -> None:
    orig = "/foo/AClass"
    cfg = OmegaConf.create({"hydra": HydraConf(runtime=RuntimeConf(cwd=orig))})
    assert isinstance(cfg, DictConfig)
    HydraConfig.instance().set_config(cfg)
    assert utils.get_original_cwd() == orig


def test_get_original_cwd_without_hydra(hydra_restore_singletons: Any) -> None:
    with raises(ValueError):
        utils.get_original_cwd()


@mark.parametrize(
    "orig_cwd, path, expected",
    [
        ("/home/omry/hydra", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "foo/bar", "/home/omry/hydra/foo/bar"),
        ("/home/omry/hydra/", "/foo/bar", "/foo/bar"),
    ],
)
def test_to_absolute_path(
    hydra_restore_singletons: Any, orig_cwd: str, path: str, expected: str
) -> None:
    # normalize paths to current OS
    orig_cwd = str(Path(orig_cwd))
    path = str(Path(path))
    expected = str(Path(expected))
    cfg = OmegaConf.create({"hydra": HydraConf(runtime=RuntimeConf(cwd=orig_cwd))})
    assert isinstance(cfg, DictConfig)
    HydraConfig().set_config(cfg)
    assert utils.to_absolute_path(path) == expected


@mark.parametrize(
    "path, expected",
    [
        ("foo/bar", f"{os.getcwd()}/foo/bar"),
        ("foo/bar", f"{os.getcwd()}/foo/bar"),
        ("/foo/bar", os.path.abspath("/foo/bar")),
    ],
)
def test_to_absolute_path_without_hydra(
    hydra_restore_singletons: Any, path: str, expected: str
) -> None:
    # normalize paths to current OS
    path = str(Path(path))
    expected = str(Path(expected).absolute())
    assert utils.to_absolute_path(path) == expected


class TestRunAndReport:
    def test_success(self) -> None:
        def func() -> Any:
            return 123

        assert run_and_report(func) == 123

    def test_simple_failure(self) -> None:
        """Full traceback is printed for simple `run_and_report` failure."""

        def simple_error() -> None:
            assert False, "simple_err_msg"

        mock_stderr = io.StringIO()
        with raises(SystemExit, match="1"), patch("sys.stderr", new=mock_stderr):
            run_and_report(simple_error)
        mock_stderr.seek(0)
        stderr_output = mock_stderr.read()
        assert_regex_match(
            dedent(
                r"""
                Traceback \(most recent call last\):$
                  File "[^"]+", line \d+, in run_and_report$
                    return func\(\)$
                  File "[^"]+", line \d+, in simple_error$
                    assert False, "simple_err_msg"$
                AssertionError: simple_err_msg$
                assert False$
                """
            ),
            stderr_output,
        )

    def test_run_job_failure(self) -> None:
        """
        If a function named `run_job` appears in the traceback, the top of the
        stack is stripped away until after the `run_job` frame.
        """

        def run_job_wrapper() -> None:
            def run_job() -> None:
                def nested_error() -> None:
                    assert False, "nested_err"

                nested_error()

            run_job()

        mock_stderr = io.StringIO()
        with raises(SystemExit, match="1"), patch("sys.stderr", new=mock_stderr):
            run_and_report(run_job_wrapper)
        mock_stderr.seek(0)
        stderr_output = mock_stderr.read()
        assert_regex_match(
            dedent(
                r"""
                Traceback \(most recent call last\):$
                  File "[^"]+", line \d+, in nested_error$
                    assert False, "nested_err"$
                AssertionError: nested_err$
                assert False$
                Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\.$
                """
            ),
            stderr_output,
        )

    def test_run_job_omegaconf_failure(self) -> None:
        """
        If a function named `run_job` appears in the traceback, the bottom of the
        stack is stripped away until an `omegaconf` frame is found.
        """

        def run_job() -> None:
            def job_calling_omconf() -> None:
                from omegaconf import OmegaConf

                OmegaConf.resolve(123)  # type: ignore

            job_calling_omconf()

        mock_stderr = io.StringIO()
        with raises(SystemExit, match="1"), patch("sys.stderr", new=mock_stderr):
            run_and_report(run_job)
        mock_stderr.seek(0)
        stderr_output = mock_stderr.read()
        print(f"stderr_output:\n{stderr_output}\n--------")
        assert_regex_match(
            dedent(
                r"""
                Traceback \(most recent call last\):$
                  File "[^"]+", line \d+, in job_calling_omconf$
                    OmegaConf.resolve\(123\)  # type: ignore$
                ValueError: Invalid config type \(int\), expected an OmegaConf Container$
                Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\.$
                """
            ),
            stderr_output,
        )
