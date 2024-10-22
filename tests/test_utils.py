# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import io
import json
import os
import re
from pathlib import Path
from textwrap import dedent
from typing import Any, NoReturn, Optional
from unittest.mock import patch

from omegaconf import DictConfig, OmegaConf
from pytest import mark, param, raises, warns

from hydra import utils
from hydra._internal.deprecation_warning import deprecation_warning
from hydra._internal.utils import run_and_report
from hydra.conf import HydraConf, RuntimeConf
from hydra.core.hydra_config import HydraConfig
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.errors import HydraDeprecationError
from hydra.test_utils.test_utils import (
    assert_multiline_regex_search,
    assert_regex_match,
)


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


@mark.parametrize(
    "obj",
    [
        ("foo bar"),
        (10),
        ({"foo": '\\"bar\\\'"'}),
        ([1, 2, "3", {"a": "xyz"}]),
        ({"a": 10, "b": "c", "d": {"e": [1, 2, "3"], "f": ["g", {"h": {"i": "j"}}]}}),
        (
            {
                "a": 10,
                "b": "c\nnl",
                "d": {"e": [1, 2, "3"], "f": ["g", {"h": {"i": "j"}}]},
            }
        ),
        ({"json_val": json.dumps({"a": 10, "b": "c\\\nnl"}, indent=4)}),
    ],
)
def test_to_hydra_override_value_str_roundtrip(
    hydra_restore_singletons: Any, obj: Any
) -> None:
    override_str = utils.to_hydra_override_value_str(obj)
    override_params = f"++ov={override_str}"
    o = OverridesParser.create().parse_override(override_params)
    assert o.value() == obj


@mark.parametrize(
    "env_setting,expected_error",
    [
        param(None, False, id="env_unset"),
        param("", False, id="env_empty"),
        param("1", True, id="env_set"),
    ],
)
def test_deprecation_warning(
    monkeypatch: Any, env_setting: Optional[str], expected_error: bool
) -> None:
    msg = "Feature FooBar is deprecated"
    if env_setting is not None:
        monkeypatch.setenv("HYDRA_DEPRECATION_WARNINGS_AS_ERRORS", env_setting)
    if expected_error:
        with raises(HydraDeprecationError, match=re.escape(msg)):
            deprecation_warning(msg)
    else:
        with warns(UserWarning, match=re.escape(msg)):
            deprecation_warning(msg)


class TestRunAndReport:
    """
    Test the `hydra._internal.utils.run_and_report` function.

    def run_and_report(func: Any) -> Any: ...

    This class defines several test methods:
      test_success:
          a simple test case where `run_and_report(func)` succeeds.
      test_failure:
          test when `func` raises an exception, and `run_and_report(func)`
          prints a nicely-formatted error message
      test_simplified_traceback_failure:
          test when printing a nicely-formatted error message fails, so
          `run_and_report` falls back to re-raising the exception from `func`.
    """

    class DemoFunctions:
        """
        The methods of this `DemoFunctions` class are passed to
        `run_and_report` as the func argument.
        """

        @staticmethod
        def success_func() -> Any:
            return 123

        @staticmethod
        def simple_error() -> None:
            assert False, "simple_err_msg"

        @staticmethod
        def run_job_wrapper() -> None:
            """
            Trigger special logic in `run_and_report` that looks for a function
            called "run_job" in the stack and strips away the leading stack
            frames.
            """

            def run_job() -> None:
                def nested_error() -> None:
                    assert False, "nested_err"

                nested_error()

            run_job()

        @staticmethod
        def omegaconf_job_wrapper() -> None:
            """
            Trigger special logic in `run_and_report` that looks for the
            `omegaconf` module in the stack and strips away the bottom stack
            frames.
            """

            def run_job() -> None:
                def job_calling_omconf() -> None:
                    from omegaconf import OmegaConf

                    # The below causes an exception:
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
                    Traceback \(most recent call last\):
                      File "[^"]+", line \d+, in run_and_report
                        return func\(\)(
                               \^+)?
                      File "[^"]+", line \d+, in simple_error
                        assert False, "simple_err_msg"
                    AssertionError: simple_err_msg
                    assert False
                    """
                ).strip(),
                id="simple_failure_full_traceback",
            ),
            param(
                DemoFunctions.run_job_wrapper,
                dedent(
                    r"""
                    Traceback \(most recent call last\):
                      File "[^"]+", line \d+, in nested_error
                        assert False, "nested_err"
                    AssertionError: nested_err
                    assert False

                    Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\.
                    """
                ).strip(),
                id="strip_run_job_from_top_of_stack",
            ),
            param(
                DemoFunctions.omegaconf_job_wrapper,
                dedent(
                    r"""
                    Traceback \(most recent call last\):
                      File "[^"]+", line \d+, in job_calling_omconf
                        OmegaConf.resolve\(123\)  # type: ignore(
                        \^+)?
                    ValueError: Invalid config type \(int\), expected an OmegaConf Container

                    Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\.
                    """
                ).strip(),
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
        assert_multiline_regex_search(expected_traceback_regex, stderr_output)

    def test_simplified_traceback_with_no_module(self) -> None:
        """
        Test that simplified traceback logic can succeed even if
        `inspect.getmodule(frame)` returns `None` for one of
        the frames in the stacktrace.
        """
        demo_func = self.DemoFunctions.run_job_wrapper
        expected_traceback_regex = dedent(
            r"""
            Traceback \(most recent call last\):$
              File "[^"]+", line \d+, in nested_error$
                assert False, "nested_err"$
            AssertionError: nested_err$
            assert False$
            Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\.$
            """
        )
        mock_stderr = io.StringIO()
        with raises(SystemExit, match="1"), patch("sys.stderr", new=mock_stderr):
            # Patch `inspect.getmodule` so that it will return None. This simulates a
            # situation where a python module cannot be identified from a traceback
            # stack frame. This can occur when python extension modules or
            # multithreading are involved.
            with patch("inspect.getmodule", new=lambda *args: None):
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

        def throws(*args: Any, **kwargs: Any) -> NoReturn:
            assert False, "Error thrown"

        expected_traceback_regex = dedent(
            r"""
            An error occurred during Hydra's exception formatting:$
            AssertionError\(.*Error thrown.*\)$
            """
        )
        mock_stderr = io.StringIO()
        with raises(AssertionError, match="nested_err"), patch(
            "sys.stderr", new=mock_stderr
        ):
            # patch `traceback.print_exception` so that an exception will occur
            # in the simplified traceback logic:
            with patch("traceback.print_exception", new=throws):
                run_and_report(demo_func)
        mock_stderr.seek(0)
        stderr_output = mock_stderr.read()
        assert_regex_match(expected_traceback_regex, stderr_output)
