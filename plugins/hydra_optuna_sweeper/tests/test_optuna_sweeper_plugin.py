# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from typing import Any, List

import pytest
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import (
    TSweepRunner,
    chdir_plugin_root,
    run_python_script,
)
from omegaconf import DictConfig, OmegaConf
from optuna.distributions import (
    BaseDistribution,
    CategoricalDistribution,
    DiscreteUniformDistribution,
    IntLogUniformDistribution,
    IntUniformDistribution,
    LogUniformDistribution,
    UniformDistribution,
)

from hydra_plugins.hydra_optuna_sweeper import _impl
from hydra_plugins.hydra_optuna_sweeper.optuna_sweeper import OptunaSweeper

chdir_plugin_root()


# https://github.com/pyreadline/pyreadline/issues/65
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_discovery() -> None:
    assert OptunaSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


def check_distribution(expected: BaseDistribution, actual: BaseDistribution) -> None:
    if not isinstance(expected, CategoricalDistribution):
        assert expected == actual
        return

    assert isinstance(actual, CategoricalDistribution)
    # shuffle() will randomize the order of items in choices.
    assert set(expected.choices) == set(actual.choices)


# https://github.com/pyreadline/pyreadline/issues/65
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {"type": "categorical", "choices": [1, 2, 3]},
            CategoricalDistribution([1, 2, 3]),
        ),
        ({"type": "int", "low": 0, "high": 10}, IntUniformDistribution(0, 10)),
        (
            {"type": "int", "low": 0, "high": 10, "step": 2},
            IntUniformDistribution(0, 10, step=2),
        ),
        ({"type": "int", "low": 0, "high": 5}, IntUniformDistribution(0, 5)),
        (
            {"type": "int", "low": 1, "high": 100, "log": True},
            IntLogUniformDistribution(1, 100),
        ),
        ({"type": "float", "low": 0, "high": 1}, UniformDistribution(0, 1)),
        (
            {"type": "float", "low": 0, "high": 10, "step": 2},
            DiscreteUniformDistribution(0, 10, 2),
        ),
        (
            {"type": "float", "low": 1, "high": 100, "log": True},
            LogUniformDistribution(1, 100),
        ),
    ],
)
def test_create_optuna_distribution_from_config(input: Any, expected: Any) -> None:
    actual = _impl.create_optuna_distribution_from_config(input)
    check_distribution(expected, actual)


# https://github.com/pyreadline/pyreadline/issues/65
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize(
    "input, expected",
    [
        ("key=choice(1,2)", CategoricalDistribution([1, 2])),
        ("key=choice(true, false)", CategoricalDistribution([True, False])),
        ("key=choice('hello', 'world')", CategoricalDistribution(["hello", "world"])),
        ("key=shuffle(range(1,3))", CategoricalDistribution((1, 2))),
        ("key=range(1,3)", IntUniformDistribution(1, 3)),
        ("key=interval(1, 5)", UniformDistribution(1, 5)),
        ("key=int(interval(1, 5))", IntUniformDistribution(1, 5)),
        ("key=tag(log, interval(1, 5))", LogUniformDistribution(1, 5)),
        ("key=tag(log, int(interval(1, 5)))", IntLogUniformDistribution(1, 5)),
    ],
)
def test_create_optuna_distribution_from_override(input: Any, expected: Any) -> None:
    parser = OverridesParser.create()
    parsed = parser.parse_overrides([input])[0]
    actual = _impl.create_optuna_distribution_from_override(parsed)
    check_distribution(expected, actual)


# https://github.com/pyreadline/pyreadline/issues/65
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_launch_jobs(hydra_sweep_runner: TSweepRunner) -> None:
    sweep = hydra_sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs",
        config_name="compose.yaml",
        task_function=None,
        overrides=[
            "hydra/sweeper=optuna",
            "hydra/launcher=basic",
            "hydra.sweeper.optuna_config.n_trials=8",
            "hydra.sweeper.optuna_config.n_jobs=3",
        ],
    )
    with sweep:
        assert sweep.returns is None


# https://github.com/pyreadline/pyreadline/issues/65
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize("with_commandline", (True, False))
def test_optuna_example(with_commandline: bool, tmpdir: Path) -> None:
    cmd = [
        "example/sphere.py",
        "--multirun",
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra.sweeper.optuna_config.n_trials=20",
        "hydra.sweeper.optuna_config.n_jobs=8",
        "hydra.sweeper.optuna_config.sampler=random",
        "hydra.sweeper.optuna_config.seed=123",
    ]
    if with_commandline:
        cmd += [
            "x=choice(0, 1, 2)",
            "y=0",  # Fixed parameter
        ]
    run_python_script(cmd)
    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")
    assert isinstance(returns, DictConfig)
    assert returns.name == "optuna"
    assert returns["best_params"]["x"] == 0
    if with_commandline:
        assert "y" not in returns["best_params"]
    else:
        assert returns["best_params"]["y"] == 0
    assert returns["best_value"] == 0


# https://github.com/pyreadline/pyreadline/issues/65
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize("with_commandline", (True, False))
def test_optuna_multi_objective_example(with_commandline: bool, tmpdir: Path) -> None:
    cmd = [
        "example/multi-objective.py",
        "--multirun",
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra.sweeper.optuna_config.n_trials=20",
        "hydra.sweeper.optuna_config.n_jobs=1",
        "hydra.sweeper.optuna_config.sampler=random",
        "hydra.sweeper.optuna_config.seed=123",
    ]
    if with_commandline:
        cmd += [
            "x=range(0, 5)",
            "y=range(0, 3)",
        ]
    run_python_script(cmd)
    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")
    assert isinstance(returns, DictConfig)
    assert returns.name == "optuna"
    if with_commandline:
        for trial_x in returns["solutions"]:
            assert trial_x["params"]["x"] % 1 == 0
            assert trial_x["params"]["y"] % 1 == 0
            # The trials must not dominate each other.
            for trial_y in returns["solutions"]:
                assert not _dominates(trial_x, trial_y)
    else:
        for trial_x in returns["solutions"]:
            assert trial_x["params"]["x"] % 1 in {0, 0.5}
            assert trial_x["params"]["y"] % 1 in {0, 0.5}
            # The trials must not dominate each other.
            for trial_y in returns["solutions"]:
                assert not _dominates(trial_x, trial_y)


def _dominates(values_x: List[float], values_y: List[float]) -> bool:
    return all(x <= y for x, y in zip(values_x, values_y)) and any(
        x < y for x, y in zip(values_x, values_y)
    )
