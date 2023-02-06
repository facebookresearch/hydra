# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from pathlib import Path
from typing import Callable, Generator, List, Optional

from pytest import fixture

from hydra.core.singleton import Singleton
from hydra.test_utils.test_utils import SweepTaskFunction, TaskTestFunction
from hydra.types import TaskFunction


@fixture(scope="function")
def hydra_restore_singletons() -> Generator[None, None, None]:
    """
    Restore singletons state after the function returns
    """
    state = copy.deepcopy(Singleton.get_state())
    yield
    Singleton.set_state(state)


@fixture(scope="function")
def hydra_sweep_runner() -> (
    Callable[
        [
            Optional[str],
            Optional[str],
            Optional[TaskFunction],
            Optional[str],
            Optional[str],
            Optional[List[str]],
            Optional[Path],
            bool,
        ],
        SweepTaskFunction,
    ]
):
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        task_function: Optional[TaskFunction],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]],
        temp_dir: Optional[Path] = None,
        configure_logging: bool = False,
    ) -> SweepTaskFunction:
        sweep = SweepTaskFunction()
        sweep.calling_file = calling_file
        sweep.calling_module = calling_module
        sweep.task_function = task_function
        sweep.config_path = config_path
        sweep.config_name = config_name
        sweep.overrides = overrides or []
        sweep.temp_dir = str(temp_dir)
        sweep.configure_logging = configure_logging
        return sweep

    return _


@fixture(scope="function")
def hydra_task_runner() -> (
    Callable[
        [
            Optional[str],
            Optional[str],
            Optional[str],
            Optional[str],
            Optional[List[str]],
            bool,
        ],
        TaskTestFunction,
    ]
):
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        config_path: Optional[str],
        config_name: Optional[str],
        overrides: Optional[List[str]] = None,
        configure_logging: bool = False,
    ) -> TaskTestFunction:
        task = TaskTestFunction()
        task.overrides = overrides or []
        task.calling_file = calling_file
        task.config_name = config_name
        task.calling_module = calling_module
        task.config_path = config_path
        task.configure_logging = configure_logging
        return task

    return _
