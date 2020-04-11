# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from typing import Any, Callable, List, Optional

import pytest

from hydra.core.singleton import Singleton
from hydra.test_utils.test_utils import (
    GlobalHydraContext,
    SweepTaskFunction,
    TaskTestFunction,
)
from hydra.types import TaskFunction


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
