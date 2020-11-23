# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from typing import Any

import pytest
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root, get_run_output
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


@pytest.mark.parametrize(  # type: ignore
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


@pytest.mark.parametrize(  # type: ignore
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


@pytest.mark.parametrize("with_commandline", (True, False))  # type: ignore
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
    get_run_output(cmd)
    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")
    assert isinstance(returns, DictConfig)
    assert returns.name == "optuna"
    assert returns["best_params"]["x"] == 0
    if with_commandline:
        assert "y" not in returns["best_params"]
    else:
        assert returns["best_params"]["y"] == 0
    assert returns["best_value"] == 0
