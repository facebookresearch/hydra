# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import importlib
import math
from typing import Any, Callable, List, Optional

import pytest
from omegaconf import DictConfig

from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import TSweepRunner  # noqa: F401
from hydra.test_utils.test_utils import SweepTaskFunction
from hydra_plugins.hydra_ax_sweeper import AxSweeper


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

    def __init__(self) -> None:
        super().__init__()
        self.calling_function = None

    def __call__(self, cfg: DictConfig) -> Any:
        """
        Actual function being executed by Hydra
        """
        assert self.calling_function is not None
        return self.calling_function(cfg=cfg)

    def __enter__(self) -> "SweepTaskFunction":
        assert self.calling_module is not None
        module = importlib.import_module(self.calling_module)
        self.calling_function = getattr(module, "banana")
        return super().__enter__()


@pytest.fixture(scope="function")  # type: ignore
def ax_sweep_runner() -> Callable[
    [Optional[str], Optional[str], Optional[str], Optional[List[str]], Optional[bool]],
    AxSweepTaskFunction,
]:
    def _(
        calling_file: Optional[str],
        calling_module: Optional[str],
        config_path: Optional[str],
        overrides: Optional[List[str]],
        strict: Optional[bool] = None,
    ) -> AxSweepTaskFunction:
        sweep = AxSweepTaskFunction()
        sweep.calling_file = calling_file
        sweep.calling_module = calling_module
        sweep.config_path = config_path
        sweep.strict = strict
        sweep.overrides = overrides or []
        return sweep

    return _


def test_launched_jobs(
    ax_sweep_runner: TSweepRunner,
) -> None:  # noqa: F811 # type: ignore
    sweep = ax_sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.ax_sweeper_plugin",
        config_path="configs/ax_sweeper_plugin/banana.yaml",
        overrides=["hydra/sweeper=ax", "hydra/launcher=basic"],
        strict=True,
    )
    with sweep:
        assert sweep.returns is not None
        assert len(sweep.returns) == 2
        best_parameters, predictions = sweep.returns
        assert len(best_parameters) == 2
        assert math.isclose(best_parameters["banana.x"], 1.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["banana.y"], 1.0, abs_tol=1e-4)
        assert math.isclose(predictions[0]["objective"], 0.7, abs_tol=1e-1)
