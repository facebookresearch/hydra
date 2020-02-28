# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Utilities used by tests
"""
import copy
import logging
import os
import shutil
import string
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator, List, Optional, Union

import pytest
from omegaconf import DictConfig, OmegaConf
from typing_extensions import Protocol

import hydra.experimental
from hydra._internal.hydra import Hydra
from hydra.core.global_hydra import GlobalHydra
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, split_config_path
from hydra.types import TaskFunction

# CircleCI does not have the environment variable USER, breaking the tests.
os.environ["USER"] = "test_user"

log = logging.getLogger(__name__)


@contextmanager
def does_not_raise(enter_result: Any = None) -> Iterator[Any]:
    yield enter_result


class GlobalHydraContext:
    def __init__(self) -> None:
        self.task_name: Optional[str] = None
        self.config_dir: Optional[str] = None
        self.strict: Optional[bool] = None

    def __enter__(self) -> "GlobalHydraContext":
        hydra.experimental.initialize(
            config_dir=self.config_dir, strict=self.strict, caller_stack_depth=2
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        GlobalHydra().clear()


@pytest.fixture(scope="function")  # type: ignore
def hydra_global_context() -> Callable[
    [str, Optional[str], Optional[bool]], GlobalHydraContext
]:
    def _(
        task_name: str = "task",
        config_dir: Optional[str] = None,
        strict: Optional[bool] = False,
    ) -> "GlobalHydraContext":
        ctx = GlobalHydraContext()
        ctx.task_name = task_name
        ctx.config_dir = config_dir
        ctx.strict = strict
        return ctx

    return _


class TGlobalHydraContext(Protocol):
    def __call__(
        self,
        task_name: str = "task",
        config_dir: Optional[str] = None,
        strict: Optional[bool] = False,
    ) -> GlobalHydraContext:
        ...


"""
Task runner fixture
"""


class TaskTestFunction:
    """
    Context function
    """

    def __init__(self) -> None:
        self.temp_dir: Optional[str] = None
        self.overrides: Optional[List[str]] = None
        self.calling_file: Optional[str] = None
        self.calling_module: Optional[str] = None
        self.config_path: Optional[str] = None
        self.config_name: Optional[str] = None
        self.strict: Optional[bool] = None
        self.hydra: Optional[Hydra] = None
        self.job_ret: Optional[JobReturn] = None

    def __call__(self, cfg: DictConfig) -> Any:
        """
        Actual function being executed by Hydra
        """

        return 100

    def __enter__(self) -> "TaskTestFunction":
        try:
            config_dir, config_name = split_config_path(
                self.config_path, self.config_name
            )

            self.hydra = Hydra.create_main_hydra_file_or_module(
                calling_file=self.calling_file,
                calling_module=self.calling_module,
                config_dir=config_dir,
                strict=self.strict,
            )
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            assert overrides is not None
            overrides.append("hydra.run.dir={}".format(self.temp_dir))
            self.job_ret = self.hydra.run(
                config_name=config_name, task_function=self, overrides=overrides
            )
            return self
        finally:
            GlobalHydra().clear()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # release log file handles
        logging.shutdown()
        assert self.temp_dir is not None
        shutil.rmtree(self.temp_dir)


@pytest.fixture(scope="function")  # type: ignore
def task_runner() -> Callable[
    [
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[List[str]],
        Optional[bool],
    ],
    TaskTestFunction,
]:
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]] = None,
        strict: Optional[bool] = False,
    ) -> TaskTestFunction:
        task = TaskTestFunction()
        task.overrides = overrides or []
        task.calling_file = calling_file
        task.config_name = config_name
        task.calling_module = calling_module
        task.config_path = config_path
        task.strict = strict
        return task

    return _


class TTaskRunner(Protocol):
    def __call__(
        self,
        calling_file: Optional[str],
        calling_module: Optional[str],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]] = None,
        strict: Optional[bool] = False,
    ) -> TaskTestFunction:
        ...


"""
Sweep runner fixture
"""


class SweepTaskFunction:
    """
    Context function
    """

    def __init__(self) -> None:
        self.temp_dir: Optional[str] = None
        self.overrides: Optional[List[str]] = None
        self.calling_file: Optional[str] = None
        self.calling_module: Optional[str] = None
        self.task_function: Optional[TaskFunction] = None
        self.config_path: Optional[str] = None
        self.config_name: Optional[str] = None
        self.strict: Optional[bool] = None
        self.sweeps = None
        self.returns = None

    def __call__(self, cfg: DictConfig) -> Any:
        """
        Actual function being executed by Hydra
        """
        if self.task_function is not None:
            return self.task_function(cfg)
        return 100

    def __enter__(self) -> "SweepTaskFunction":
        self.temp_dir = tempfile.mkdtemp()
        overrides = copy.deepcopy(self.overrides)
        assert overrides is not None
        overrides.append("hydra.sweep.dir={}".format(self.temp_dir))
        try:
            config_dir, config_name = split_config_path(
                self.config_path, self.config_name
            )
            hydra_ = Hydra.create_main_hydra_file_or_module(
                calling_file=self.calling_file,
                calling_module=self.calling_module,
                config_dir=config_dir,
                strict=self.strict,
            )

            self.returns = hydra_.multirun(
                config_name=config_name, task_function=self, overrides=overrides
            )
        finally:
            GlobalHydra().clear()

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        assert self.temp_dir is not None
        shutil.rmtree(self.temp_dir)


@pytest.fixture(scope="function")  # type: ignore
def sweep_runner() -> Callable[
    [
        Optional[str],
        Optional[str],
        Optional[TaskFunction],
        Optional[str],
        Optional[str],
        Optional[List[str]],
        Optional[bool],
    ],
    SweepTaskFunction,
]:
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        task_function: Optional[TaskFunction],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]],
        strict: Optional[bool] = None,
    ) -> SweepTaskFunction:
        sweep = SweepTaskFunction()
        sweep.calling_file = calling_file
        sweep.calling_module = calling_module
        sweep.task_function = task_function
        sweep.config_path = config_path
        sweep.config_name = config_name
        sweep.strict = strict
        sweep.overrides = overrides or []
        return sweep

    return _


class TSweepRunner(Protocol):
    returns: List[List[JobReturn]]

    def __call__(
        self,
        calling_file: Optional[str],
        calling_module: Optional[str],
        task_function: Optional[TaskFunction],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]],
        strict: Optional[bool] = None,
    ) -> SweepTaskFunction:
        ...


def chdir_hydra_root() -> None:
    """
    Change the cwd to the root of the hydra project.
    used from unit tests to make them runnable from anywhere in the tree.
    """
    _chdir_to_dir_containing(target="ATTRIBUTION")


def chdir_plugin_root() -> None:
    """
    Change the cwd to the root of the plugin (location of setup.py)
    """
    _chdir_to_dir_containing(target="setup.py")


def _chdir_to_dir_containing(target: str, max_up: int = 4) -> None:
    cur = os.getcwd()
    while not os.path.exists(os.path.join(cur, target)) and max_up > 0:
        cur = os.path.relpath(os.path.join(cur, ".."))
        max_up = max_up - 1
    if max_up == 0:
        raise IOError("Could not find {} in parents of {}".format(target, os.getcwd()))
    os.chdir(cur)


def verify_dir_outputs(
    job_return: JobReturn, overrides: Optional[List[str]] = None
) -> None:
    """
    Verify that directory output makes sense
    """
    assert isinstance(job_return, JobReturn)
    assert job_return.working_dir is not None
    assert job_return.task_name is not None
    assert job_return.hydra_cfg is not None

    assert os.path.exists(
        os.path.join(job_return.working_dir, job_return.task_name + ".log")
    )
    hydra_dir = os.path.join(
        job_return.working_dir, job_return.hydra_cfg.hydra.output_subdir
    )
    assert os.path.exists(os.path.join(hydra_dir, "config.yaml"))
    assert os.path.exists(os.path.join(hydra_dir, "overrides.yaml"))
    assert OmegaConf.load(
        os.path.join(hydra_dir, "overrides.yaml")
    ) == OmegaConf.create(overrides or [])


def integration_test(
    tmpdir: Path,
    task_config: DictConfig,
    overrides: List[str],
    prints: Union[str, List[str]],
    expected_outputs: Union[str, List[str]],
    filename: str = "task.py",
) -> str:
    if isinstance(prints, str):
        prints = [prints]
    if isinstance(expected_outputs, str):
        expected_outputs = [expected_outputs]
    if isinstance(task_config, (list, dict)):
        task_config = OmegaConf.create(task_config)

    s = string.Template(
        """import hydra
import os
from hydra.core.hydra_config import HydraConfig

@hydra.main($CONFIG_PATH)
def experiment(cfg):
    with open("$OUTPUT_FILE", "w") as f:
        $PRINTS

if __name__ == "__main__":
    experiment()
"""
    )

    print_code = ""
    if prints is None or len(prints) == 0:
        print_code = "pass"
    else:
        for p in prints:
            print_code += 'f.write({} + "\\\n")'.format(p)

    config_path = ""
    if task_config is not None:
        cfg_file = tmpdir / "config.yaml"
        OmegaConf.save(task_config, str(cfg_file))
        config_path = "config_path='{}'".format("config.yaml")
    output_file = str(tmpdir / "output.txt")
    # replace Windows path separator \ with an escaped version \\
    output_file = output_file.replace("\\", "\\\\")
    code = s.substitute(
        PRINTS=print_code, CONFIG_PATH=config_path, OUTPUT_FILE=output_file
    )
    task_file = tmpdir / filename
    task_file.write_text(str(code), encoding="utf-8")
    cmd = [sys.executable, str(task_file)]
    cmd.extend(overrides)
    orig_dir = os.getcwd()
    try:
        os.chdir(str(tmpdir))
        subprocess.check_call(cmd)

        with open(output_file, "r") as f:
            file_str = f.read()
            output = str.splitlines(file_str)

        if expected_outputs is not None:
            assert len(output) == len(expected_outputs)
            for idx in range(len(output)):
                assert output[idx] == expected_outputs[idx]
        # some tests are parsing the file output for more specialized testing.
        return file_str
    finally:
        os.chdir(orig_dir)


@pytest.fixture(scope="function")  # type: ignore
def restore_singletons() -> Any:
    """
    A fixture to restore singletons state after this the function.
    This is useful for functions that are making a one-off change to singlestons that should not effect
    other tests
    """
    state = copy.deepcopy(Singleton.get_state())
    yield
    Singleton.set_state(state)
