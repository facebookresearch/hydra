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
from omegaconf import DictConfig, OmegaConf

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
    return 100 * (cfg.quadratic.x ** 2) + 1 * cfg.quadratic.y


def nested_quadratic_with_escape_char(cfg: DictConfig) -> Any:
    return 100 * (cfg.quadratic.x_arg ** 2) + 1 * cfg.quadratic.y_arg


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
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "hydra.sweeper.params.ax_config.max_trials=6",
            "hydra.sweeper.params.max_batch_size=2",
            "params=basic",
        ],
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
        config_name="config.yaml",
        overrides=["hydra/launcher=basic", "params=basic"],
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns["ax"]
        assert math.isclose(best_parameters["quadratic_x"], 0.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic_y"], -1.0, abs_tol=1e-4)


def test_jobs_configured_via_cmd(sweep_runner: TSweepRunner,) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "quadratic.x=-5:-2",
            "quadratic.y=-2:2",
            "params=basic",
        ],
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns["ax"]
        assert math.isclose(best_parameters["quadratic_x"], -2.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic_y"], 2.0, abs_tol=1e-4)


def test_jobs_configured_via_cmd_and_config(sweep_runner: TSweepRunner) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "hydra.sweeper.params.ax_config.max_trials=2",
            "quadratic.x=-5:-2",
            "params=basic",
        ],
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns["ax"]
        assert math.isclose(best_parameters["quadratic_x"], -2.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic_y"], 1.0, abs_tol=1e-4)


def test_configuration_set_via_cmd_and_default_config(
    sweep_runner: TSweepRunner,
) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "hydra.sweeper.params.ax_config.max_trials=2",
            "hydra.sweeper.params.ax_config.early_stop.max_epochs_without_improvement=2",
            "quadratic=basic",
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
        assert "quadratic_x" in best_parameters
        assert "quadratic_y" in best_parameters


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


def test_example_app(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "example/banana.py",
        "-m",
        "hydra.run.dir=" + str(tmpdir),
        "banana.x=-5:5",
        "banana.y=-5:10.1",
        "hydra.sweeper.params.ax_config.max_trials=2",
    ]
    result = subprocess.check_output(cmd).decode("utf-8").rstrip()
    assert "banana.x: range=[-5, 5], type = int" in result
    assert "banana.y: range=[-5.0, 10.1], type = float" in result


# TODO: enable this and make sure it runs reasonable fast
# # Run launcher test suite with the basic launcher and this sweeper
# @pytest.mark.parametrize(
#     "launcher_name, overrides",
#     [("basic", ["hydra/sweeper=ax", "quadratic.x=-1.0:1.0", "quadratic.y=-1.0:1.0"])],
# )
# class TestAxSweeper(LauncherTestSuite):
#     def task_function(self, cfg):
#         return 100 * (cfg.quadratic.x ** 2) + 1 * cfg.quadratic.y


@pytest.mark.parametrize(
    "overrides", [[], ["quadratic.x_arg=-1:1"]],
)
def test_jobs_configured_via_nested_config(
    sweep_runner: TSweepRunner, overrides: list,
) -> None:
    sweep = sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=nested_quadratic_with_escape_char,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "quadratic=nested_with_escape_char",
            "params=nested_with_escape_char",
        ]
        + overrides,
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns["ax"]
        assert math.isclose(best_parameters["quadratic_x_arg"], 0.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic_y_arg"], -1.0, abs_tol=1e-4)


@pytest.mark.parametrize(
    "inp, str_to_replace, str_to_replace_with, expected",
    [
        ("apple", ".", "_", "apple"),
        ("a.pple", ".", "_", "a_pple"),
        ("a.p.ple", ".", "_", "a_p_ple"),
        (r"a\.pple", ".", "_", "a.pple"),
        (r"a.p\.pl.e", ".", "_", "a_p.pl_e"),
    ],
)
def test_process_key_method(
    inp: str, str_to_replace: str, str_to_replace_with: str, expected: str
):
    from hydra_plugins.hydra_ax_sweeper._core import normalize_key

    assert normalize_key(inp, str_to_replace, str_to_replace_with) == expected
