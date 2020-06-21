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
from typing import Any, Dict, Iterator, List, Optional, Union

from omegaconf import DictConfig, OmegaConf
from typing_extensions import Protocol

from hydra._internal.hydra import Hydra
from hydra.core.global_hydra import GlobalHydra
from hydra.core.utils import JobReturn, split_config_path
from hydra.types import TaskFunction

# CircleCI does not have the environment variable USER, breaking the tests.
os.environ["USER"] = "test_user"

log = logging.getLogger(__name__)


@contextmanager
def does_not_raise(enter_result: Any = None) -> Iterator[Any]:
    yield enter_result


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
                config_path=config_dir,
                job_name=None,
                strict=self.strict,
            )
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            assert overrides is not None
            overrides.append(f"hydra.run.dir={self.temp_dir}")
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


class TTaskRunner(Protocol):
    def __call__(
        self,
        calling_file: Optional[str],
        calling_module: Optional[str],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]] = None,
        strict: Optional[bool] = None,
    ) -> TaskTestFunction:
        ...


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
        overrides.append(f"hydra.sweep.dir={self.temp_dir}")
        try:
            config_dir, config_name = split_config_path(
                self.config_path, self.config_name
            )
            hydra_ = Hydra.create_main_hydra_file_or_module(
                calling_file=self.calling_file,
                calling_module=self.calling_module,
                config_path=config_dir,
                job_name=None,
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


def _chdir_to_dir_containing(target: str, max_up: int = 6) -> None:
    cur = os.getcwd()
    while not os.path.exists(os.path.join(cur, target)) and max_up > 0:
        cur = os.path.relpath(os.path.join(cur, ".."))
        max_up = max_up - 1
    if max_up == 0:
        raise IOError(f"Could not find {target} in parents of {os.getcwd()}")
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


def _get_statements(indent: str, statements: Union[None, str, List[str]]) -> str:
    if isinstance(statements, str):
        statements = [statements]

    code = ""
    if statements is None or len(statements) == 0:
        code = "pass"
    else:
        for p in statements:
            code += f"{indent}{p}\n"
    return code


def integration_test(
    tmpdir: Path,
    task_config: DictConfig,
    overrides: List[str],
    prints: Union[str, List[str]],
    expected_outputs: Union[str, List[str]],
    prolog: Union[None, str, List[str]] = None,
    filename: str = "task.py",
    env_override: Dict[str, str] = {},
    clean_environment: bool = False,
) -> str:
    if isinstance(expected_outputs, str):
        expected_outputs = [expected_outputs]
    if isinstance(task_config, (list, dict)):
        task_config = OmegaConf.create(task_config)
    if isinstance(prints, str):
        prints = [prints]
    prints = [f'f.write({p} + "\\n")' for p in prints]

    s = string.Template(
        """import hydra
import os
from hydra.core.hydra_config import HydraConfig

$PROLOG

@hydra.main($CONFIG_NAME)
def experiment(cfg):
    with open("$OUTPUT_FILE", "w") as f:
$PRINTS

if __name__ == "__main__":
    experiment()
"""
    )

    print_code = _get_statements(indent="        ", statements=prints)
    prolog_code = _get_statements(indent="", statements=prolog)

    config_name = ""
    if task_config is not None:
        cfg_file = tmpdir / "config.yaml"
        with open(str(cfg_file), "w") as f:
            f.write("# @package _global_\n")
            OmegaConf.save(task_config, f)
        config_name = "config_name='config'"
    output_file = str(tmpdir / "output.txt")
    # replace Windows path separator \ with an escaped version \\
    output_file = output_file.replace("\\", "\\\\")
    code = s.substitute(
        PRINTS=print_code,
        CONFIG_NAME=config_name,
        OUTPUT_FILE=output_file,
        PROLOG=prolog_code,
    )
    task_file = tmpdir / filename
    task_file.write_text(str(code), encoding="utf-8")
    cmd = [sys.executable, str(task_file)]
    cmd.extend(overrides)
    orig_dir = os.getcwd()
    try:
        os.chdir(str(tmpdir))
        if clean_environment:
            modified_env = {}
        else:
            modified_env = os.environ.copy()
            modified_env.update(env_override)
        subprocess.check_call(cmd, env=modified_env)

        with open(output_file, "r") as f:
            file_str = f.read()
            output = str.splitlines(file_str)

        if expected_outputs is not None:
            assert len(output) == len(
                expected_outputs
            ), f"Unexpected number of output lines from {task_file}, output lines:\n\n{file_str}"
            for idx in range(len(output)):
                assert (
                    output[idx] == expected_outputs[idx]
                ), f"Unexpected output for {prints[idx]} : expected {expected_outputs[idx]}, got {output[idx]}"
        # some tests are parsing the file output for more specialized testing.
        return file_str
    finally:
        os.chdir(orig_dir)
