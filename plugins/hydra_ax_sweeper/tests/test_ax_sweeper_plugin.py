# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
import os
from typing import Any

import yaml
from omegaconf import DictConfig

from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import TSweepRunner, sweep_runner  # noqa: F401
from hydra_plugins.hydra_ax_sweeper import AxSweeper


def test_discovery() -> None:
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert AxSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


def banana(cfg: DictConfig) -> Any:
    x = cfg.banana.x
    y = cfg.banana.y
    a = 1
    b = 100
    z = (a - x) ** 2 + b * ((y - x ** 2) ** 2)
    return z


def test_launched_jobs(sweep_runner: TSweepRunner,) -> None:  # noqa: F811
    sweep = sweep_runner(
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
        assert sweep.returns is None
        with open(f"{sweep.temp_dir}/optimization_results.yaml", "r") as f:
            returns = yaml.safe_load(f)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters, predictions = returns["ax"]
        assert len(best_parameters) == 2
        assert math.isclose(best_parameters["banana.x"], 3.0, abs_tol=1e-1)
        assert math.isclose(best_parameters["banana.y"], 9.97630435, abs_tol=1e-1)
