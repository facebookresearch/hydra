# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from hydra.core.hydra_config import HydraConfig
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root
from hydra_plugins.hydra_ax_sweeper.ax_sweeper import AxSweeper

chdir_plugin_root()


def test_discovery() -> None:
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert AxSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


def quadratic(cfg: DictConfig) -> Any:
    x = cfg.quadratic.x
    y = cfg.quadratic.y
    a = 100
    b = 1
    z = a * (x ** 2) + b * y
    return z


@pytest.mark.parametrize(
    "n,expected",
    [
        (None, [[1, 2, 3, 4, 5]]),
        (1, [[1], [2], [3], [4], [5]]),
        (2, [[1, 2], [3, 4], [5]]),
        (5, [[1, 2, 3, 4, 5]]),
        (6, [[1, 2, 3, 4, 5]]),
    ],
)
def test_chunk_method_for_valid_inputs(n, expected):
    from hydra_plugins.hydra_ax_sweeper._core import CoreAxSweeper

    chunk_func = CoreAxSweeper.chunks
    batch = [1, 2, 3, 4, 5]
    out = list(chunk_func(batch, n))
    print(expected)
    assert out == expected


@pytest.mark.parametrize("n", [-1, -11, 0])
def test_chunk_method_for_invalid_inputs(n):
    from hydra_plugins.hydra_ax_sweeper._core import CoreAxSweeper

    chunk_func = CoreAxSweeper.chunks
    batch = [1, 2, 3, 4, 5]
    with pytest.raises(ValueError):
        list(chunk_func(batch, n))


def test_jobs_dirs(sweep_runner: TSweepRunner) -> None:
    # Verify that the spawned jobs are not overstepping the directories of one another.
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="quadratic.yaml",
        overrides=[
            "hydra/launcher=basic",
            "hydra/sweeper=ax",
            "hydra.sweeper.params.ax_config.client.random_seed=1",
            "hydra.sweeper.params.ax_config.max_trials=6",
            "hydra.sweeper.params.max_batch_size=2",
        ],
        strict=True,
    )
    with sweep:
        assert isinstance(sweep.temp_dir, str)
        dirs = [
            x
            for x in os.listdir(sweep.temp_dir)
            if os.path.isdir(os.path.join(sweep.temp_dir, x))
        ]
        assert len(dirs) == 6  # and a total of 6 unique output directories


def test_jobs_configured_via_config(sweep_runner: TSweepRunner) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="quadratic.yaml",
        overrides=[
            "hydra/sweeper=ax",
            "hydra/launcher=basic",
            "hydra.sweeper.params.ax_config.client.random_seed=1",
            "hydra.sweeper.params.ax_config.max_trials=2",
        ],
        strict=True,
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns["ax"]
        assert len(best_parameters) == 2
        assert math.isclose(best_parameters["quadratic.x"], 0.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic.y"], -1.0, abs_tol=1e-4)


def test_jobs_configured_via_cmd(sweep_runner: TSweepRunner,) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="quadratic.yaml",
        overrides=[
            "hydra/sweeper=ax",
            "hydra/launcher=basic",
            "hydra.sweeper.params.ax_config.client.random_seed=1",
            "quadratic.x=-5:-2",
            "quadratic.y=-2:2",
            "hydra.sweeper.params.ax_config.max_trials=2",
        ],
        strict=True,
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns["ax"]
        assert len(best_parameters) == 2
        assert math.isclose(best_parameters["quadratic.x"], -2.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic.y"], 2.0, abs_tol=1e-4)


def test_jobs_configured_via_cmd_and_config(sweep_runner: TSweepRunner) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="quadratic.yaml",
        overrides=[
            "hydra/sweeper=ax",
            "hydra/launcher=basic",
            "hydra.sweeper.params.ax_config.client.random_seed=1",
            "quadratic.x=-5:-2",
            "hydra.sweeper.params.ax_config.max_trials=2",
        ],
        strict=True,
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns["ax"]
        assert len(best_parameters) == 2
        assert math.isclose(best_parameters["quadratic.x"], -2.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic.y"], 1.0, abs_tol=1e-4)


def test_configuration_set_via_cmd_and_default_config(
    sweep_runner: TSweepRunner,
) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="default_quadratic.yaml",
        overrides=[
            "hydra/sweeper=ax",
            "hydra/launcher=basic",
            "hydra.sweeper.params.ax_config.client.random_seed=1",
            "hydra.sweeper.params.ax_config.max_trials=2",
            "hydra.sweeper.params.ax_config.early_stop.max_epochs_without_improvement=2",
            "quadratic.x=-5:-2",
            "quadratic.y=-1:1",
        ],
    )
    with sweep:
        ax_config = HydraConfig.get().sweeper.params.ax_config
        assert ax_config.max_trials == 2
        assert ax_config.early_stop.max_epochs_without_improvement == 2
        assert ax_config.experiment.minimize is True
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        best_parameters = returns["ax"]
        assert "quadratic.x" in best_parameters
        assert "quadratic.y" in best_parameters


def test_ax_logging(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "tests/apps/polynomial.py",
        "-m",
        "hydra.run.dir=" + str(tmpdir),
        "polynomial.x=-5:-2",
        "polynomial.y=-1,1",
        "polynomial.z=10",
        "hydra.sweeper.params.ax_config.max_trials=2",
    ]
    result = subprocess.check_output(cmd).decode("utf-8").rstrip()
    assert "polynomial.x: range=[-5, -2], type = int" in result
    assert "polynomial.y: choice=[-1, 1], type = int" in result
    assert "polynomial.z: fixed=10, type = int" in result
