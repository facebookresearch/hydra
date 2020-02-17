# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
import os
from typing import Any, Callable, List, Optional

import pytest
import yaml
from omegaconf import DictConfig

from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import TSweepRunner  # noqa: F401
from hydra.test_utils.test_utils import SweepTaskFunction
from hydra.types import TaskFunction
from hydra_plugins.hydra_ax_sweeper import AxSweeper  # type: ignore


def test_discovery() -> None:
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert AxSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


class AxSweepTaskFunction(SweepTaskFunction):
    """
    Context function
    """

    def __enter__(self) -> "SweepTaskFunction":
        super().__enter__()
        with open(f"{self.temp_dir}/optimization_results.yaml", "r") as f:
            self.returns = yaml.safe_load(f)
        return self


@pytest.fixture(scope="function")  # type: ignore
def ax_sweep_runner() -> Callable[
    [
        Optional[str],
        Optional[str],
        Optional[TaskFunction],
        Optional[str],
        Optional[List[str]],
        Optional[bool],
    ],
    AxSweepTaskFunction,
]:
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        task_function: Optional[TaskFunction],
        config_path: Optional[str],
        overrides: Optional[List[str]],
        strict: Optional[bool] = None,
    ) -> AxSweepTaskFunction:
        sweep = AxSweepTaskFunction()
        sweep.calling_file = calling_file
        sweep.calling_module = calling_module
        sweep.task_function = task_function
        sweep.config_path = config_path
        sweep.strict = strict
        sweep.overrides = overrides or []
        return sweep

    return _


def banana(cfg: DictConfig) -> Any:
    x = cfg.banana.x
    y = cfg.banana.y
    a = 1
    b = 100
    z = (a - x) ** 2 + b * ((y - x ** 2) ** 2)
    return z


def test_launched_jobs(
    ax_sweep_runner: TSweepRunner,
) -> None:  # noqa: F811 # type: ignore
    sweep = ax_sweep_runner(
        calling_file=os.path.dirname(os.path.abspath(__file__)),
        calling_module=None,
        task_function=banana,
        config_path="tests/config/banana.yaml",
        overrides=[
            "hydra/sweeper=ax",
            "hydra/launcher=basic",
            "hydra.sweeper.params.random_seed=1",
        ],
        strict=True,
    )
    with sweep:
        assert sweep.returns is not None
        returns = sweep.returns["ax"]["best_parameters"]
        assert len(returns) == 2
        best_parameters, predictions = returns
        assert len(best_parameters) == 2
        assert math.isclose(best_parameters["banana.x"], 1.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["banana.y"], 0.96, abs_tol=1e-1)
        assert math.isclose(predictions[0]["objective"], -37.06, abs_tol=1)
