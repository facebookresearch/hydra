# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
import os
from pathlib import Path
from typing import Any, List

from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import (
    TSweepRunner,
    chdir_plugin_root,
    run_python_script,
)
from omegaconf import DictConfig, OmegaConf
from pytest import mark, raises

from hydra_plugins.hydra_ax_sweeper.ax_sweeper import AxSweeper  # type: ignore

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


@mark.parametrize(
    "n,expected",
    [
        (None, [[1, 2, 3, 4, 5]]),
        (1, [[1], [2], [3], [4], [5]]),
        (2, [[1, 2], [3, 4], [5]]),
        (5, [[1, 2, 3, 4, 5]]),
        (6, [[1, 2, 3, 4, 5]]),
    ],
)
def test_chunk_method_for_valid_inputs(n: int, expected: List[List[int]]) -> None:
    from hydra_plugins.hydra_ax_sweeper._core import CoreAxSweeper  # type: ignore

    chunk_func = CoreAxSweeper.chunks
    batch = [1, 2, 3, 4, 5]
    out = list(chunk_func(batch, n))
    assert out == expected


@mark.parametrize("n", [-1, -11, 0])
def test_chunk_method_for_invalid_inputs(n: int) -> None:
    from hydra_plugins.hydra_ax_sweeper._core import CoreAxSweeper

    chunk_func = CoreAxSweeper.chunks
    batch = [1, 2, 3, 4, 5]
    with raises(ValueError):
        list(chunk_func(batch, n))


def test_jobs_dirs(hydra_sweep_runner: TSweepRunner) -> None:
    # Verify that the spawned jobs are not overstepping the directories of one another.
    sweep = hydra_sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "hydra.sweeper.ax_config.max_trials=6",
            "hydra.sweeper.max_batch_size=2",
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


def test_jobs_configured_via_config(hydra_sweep_runner: TSweepRunner) -> None:
    sweep = hydra_sweep_runner(
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
        best_parameters = returns.ax
        assert math.isclose(best_parameters["quadratic.x"], 0.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic.y"], -1.0, abs_tol=1e-4)


def test_jobs_configured_via_cmd(hydra_sweep_runner: TSweepRunner) -> None:
    sweep = hydra_sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "quadratic.x=int(interval(-5, -2))",
            "quadratic.y=int(interval(-2, 2))",
            "params=basic",
        ],
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns.ax
        assert math.isclose(best_parameters["quadratic.x"], -2.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic.y"], 2.0, abs_tol=1e-4)


def test_jobs_configured_via_cmd_and_config(hydra_sweep_runner: TSweepRunner) -> None:
    sweep = hydra_sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "hydra.sweeper.ax_config.max_trials=2",
            "quadratic.x=int(interval(-5, -2))",
            "params=basic",
        ],
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        assert returns["optimizer"] == "ax"
        assert len(returns) == 2
        best_parameters = returns.ax
        assert math.isclose(best_parameters["quadratic.x"], -2.0, abs_tol=1e-4)
        assert math.isclose(best_parameters["quadratic.y"], 1.0, abs_tol=1e-4)


def test_configuration_set_via_cmd_and_default_config(
    hydra_sweep_runner: TSweepRunner,
) -> None:
    sweep = hydra_sweep_runner(
        calling_file="tests/test_ax_sweeper_plugin.py",
        calling_module=None,
        task_function=quadratic,
        config_path="config",
        config_name="config.yaml",
        overrides=[
            "hydra/launcher=basic",
            "hydra.sweeper.ax_config.max_trials=2",
            "hydra.sweeper.ax_config.early_stop.max_epochs_without_improvement=2",
            "quadratic=basic",
            "quadratic.x=interval(-5, -2)",
            "quadratic.y=interval(-1, 1)",
        ],
    )
    with sweep:
        assert sweep.returns is None
        returns = OmegaConf.load(f"{sweep.temp_dir}/optimization_results.yaml")
        assert isinstance(returns, DictConfig)
        best_parameters = returns.ax
        assert "quadratic.x" in best_parameters
        assert "quadratic.y" in best_parameters


@mark.parametrize(
    "cmd_arg, expected_str",
    [
        ("polynomial.y=choice(-1, 0, 1)", "polynomial.y: choice=[-1, 0, 1]"),
        ("polynomial.y=range(-1, 2)", "polynomial.y: choice=[-1, 0, 1]"),
        ("polynomial.y=range(-1, 3, 1)", "polynomial.y: choice=[-1, 0, 1, 2]"),
        (
            "polynomial.y=range(-1, 2, 0.5)",
            "polynomial.y: choice=[-1.0, -0.5, 0.0, 0.5, 1.0, 1.5]",
        ),
        ("polynomial.y=int(interval(-1, 2))", "polynomial.y: range=[-1, 2]"),
        ("polynomial.y=interval(-1, 2)", "polynomial.y: range=[-1.0, 2.0]"),
        ("polynomial.y=2", "polynomial.y: fixed=2"),
        ("polynomial.y=2.0", "polynomial.y: fixed=2.0"),
    ],
)
def test_ax_logging(tmpdir: Path, cmd_arg: str, expected_str: str) -> None:
    cmd = [
        "tests/apps/polynomial.py",
        "-m",
        "hydra.run.dir=" + str(tmpdir),
        "polynomial.x=interval(-5, -2)",
        "polynomial.z=10",
        "hydra.sweeper.ax_config.max_trials=2",
    ] + [cmd_arg]
    result, _ = run_python_script(cmd, allow_warnings=True)
    assert "polynomial.x: range=[-5.0, -2.0]" in result
    assert expected_str in result
    assert "polynomial.z: fixed=10" in result


@mark.parametrize(
    "cmd_args",
    [
        ["polynomial.y=choice(-1, 0, 1)", "polynomial.x=range(2,4)"],
        ["polynomial.y=1", "polynomial.x=range(2,4)"],
    ],
)
def test_search_space_exhausted_exception(tmpdir: Path, cmd_args: List[str]) -> None:
    cmd = [
        "tests/apps/polynomial.py",
        "-m",
        "hydra.run.dir=" + str(tmpdir),
        "hydra.sweeper.ax_config.max_trials=2",
    ] + cmd_args
    run_python_script(cmd, allow_warnings=True)


@mark.parametrize(
    "cmd_arg, serialized_encoding, best_coefficients, best_value",
    [
        (
            "polynomial.coefficients=[-1, 0, 1],[2, 3, 4],[5, 6, 7]",
            "choice=['[-1,0,1]', '[2,3,4]', '[5,6,7]']",
            "'[-1,0,1]'",
            101.0,
        ),
        (
            "polynomial.coefficients=choice([8, 12, 11],[-1, -1, 1000], [-2, 4, 7])",
            "choice=['[8,12,11]', '[-1,-1,1000]', '[-2,4,7]']",
            "'[-2,4,7]'",
            447,
        ),
    ],
)
def test_jobs_using_choice_between_lists(
    tmpdir: Path,
    cmd_arg: str,
    serialized_encoding: str,
    best_coefficients: str,
    best_value: float,
) -> None:
    cmd = [
        "tests/apps/polynomial_with_list_coefficients.py",
        "-m",
        "hydra.run.dir=" + str(tmpdir),
        "hydra.sweeper.ax_config.max_trials=3",
    ] + [cmd_arg]
    result, _ = run_python_script(cmd, allow_warnings=True)
    assert f"polynomial.coefficients: {serialized_encoding}" in result
    assert f"'polynomial.coefficients': {best_coefficients}" in result
    assert f"New best value: {best_value}" in result


@mark.parametrize(
    "cmd_arg, serialized_encoding, best_coefficients, best_value",
    [
        (
            "+polynomial.coefficients=choice({x:-1, y:0, z:1},{x:2, y:3, z:4},{x:5, y:6, z:7})",
            "choice=['{x:-1,y:0,z:1}', '{x:2,y:3,z:4}', '{x:5,y:6,z:7}']",
            "'{x:-1,y:0,z:1}'",
            101.0,
        ),
        (
            "+polynomial.coefficients=choice({x:8, y:12, z:11},{x:-1, y:-1, z:1000}, {x:-2, y:4, z:7})",
            "choice=['{x:8,y:12,z:11}', '{x:-1,y:-1,z:1000}', '{x:-2,y:4,z:7}']",
            "'{x:-2,y:4,z:7}'}",
            447,
        ),
    ],
)
def test_jobs_using_choice_between_dicts(
    tmpdir: Path,
    cmd_arg: str,
    serialized_encoding: str,
    best_coefficients: str,
    best_value: float,
) -> None:
    cmd = [
        "tests/apps/polynomial_with_dict_coefficients.py",
        "-m",
        "hydra.run.dir=" + str(tmpdir),
        "hydra.sweeper.ax_config.max_trials=3",
    ] + [cmd_arg]
    result, _ = run_python_script(cmd, allow_warnings=True)
    assert f"polynomial.coefficients: {serialized_encoding}" in result
    assert f"'+polynomial.coefficients': {best_coefficients}" in result
    assert f"New best value: {best_value}" in result


def test_example_app(tmpdir: Path) -> None:
    cmd = [
        "example/banana.py",
        "-m",
        "hydra.run.dir=" + str(tmpdir),
        "banana.x=int(interval(-5, 5))",
        "banana.y=interval(-5, 10.1)",
        "hydra.sweeper.ax_config.max_trials=2",
    ]
    result, _ = run_python_script(cmd, allow_warnings=True)
    assert "banana.x: range=[-5, 5]" in result
    assert "banana.y: range=[-5.0, 10.1]" in result
