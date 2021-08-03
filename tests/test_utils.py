# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import io
import os
from pathlib import Path
from textwrap import dedent
from typing import Any
from unittest.mock import patch

from omegaconf import DictConfig, OmegaConf
from pytest import mark, param, raises

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
    class DemoFunctions:
        """Demo inputs for `run_and_report`"""

        @staticmethod
        def success_func() -> Any:
            return 123

        @staticmethod
        def simple_error() -> None:
            assert False, "simple_err_msg"

        @staticmethod
        def run_job_wrapper() -> None:
            def run_job() -> None:
                def nested_error() -> None:
                    assert False, "nested_err"

                nested_error()

            run_job()

        @staticmethod
        def omegaconf_job_wrapper() -> None:
            def run_job() -> None:
                def job_calling_omconf() -> None:
                    from omegaconf import OmegaConf

                    OmegaConf.resolve(123)  # type: ignore

                job_calling_omconf()

            run_job()

    def test_success(self) -> None:
        assert run_and_report(self.DemoFunctions.success_func) == 123

    @mark.parametrize(
        "demo_func, expected_traceback_regex",
        [
            param(
                DemoFunctions.simple_error,
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
                id="simple_failure_full_traceback",
            ),
            param(
                DemoFunctions.run_job_wrapper,
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
                id="strip_run_job_from_top_of_stack",
            ),
            param(
                DemoFunctions.omegaconf_job_wrapper,
                dedent(
                    r"""
                    Traceback \(most recent call last\):$
                      File "[^"]+", line \d+, in job_calling_omconf$
                        OmegaConf.resolve\(123\)  # type: ignore$
                    ValueError: Invalid config type \(int\), expected an OmegaConf Container$
                    Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\.$
                    """
                ),
                id="strip_omegaconf_from_bottom_of_stack",
            ),
        ],
    )
    def test_failure(self, demo_func: Any, expected_traceback_regex: str) -> None:
        mock_stderr = io.StringIO()
        with raises(SystemExit, match="1"), patch("sys.stderr", new=mock_stderr):
            run_and_report(demo_func)
        mock_stderr.seek(0)
        stderr_output = mock_stderr.read()
        assert_regex_match(expected_traceback_regex, stderr_output)

    def test_simplified_traceback_failure(self) -> None:
        """
        Test that a warning is printed and the original exception is re-raised
        when an exception occurs during the simplified traceback logic.
        """
        demo_func = self.DemoFunctions.run_job_wrapper
        expected_traceback_regex = dedent(
            r"""
            An error occurred during Hydra's exception formatting:$
            AssertionError\(.*\)$
            """
        )
        mock_stderr = io.StringIO()
        with raises(AssertionError, match="nested_err"), patch(
            "sys.stderr", new=mock_stderr
        ):
            # patch `inspect.getmodule` so that an exception will occur in the
            # simplified traceback logic:
            with patch("inspect.getmodule", new=lambda *args: None):
                run_and_report(demo_func)
        mock_stderr.seek(0)
        stderr_output = mock_stderr.read()
        assert_regex_match(expected_traceback_regex, stderr_output)
