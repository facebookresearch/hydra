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
    assert expected == actual


@pytest.mark.parametrize(  # type: ignore
    "input, expected",
    [
        ("key=choice(1,2)", CategoricalDistribution([1, 2])),
        ("key=choice('hello', 'world')", CategoricalDistribution(["hello", "world"])),
        ("key=range(1,3)", IntUniformDistribution(1, 3)),
        ("key=interval(1, 5)", UniformDistribution(1, 5)),
        ("key=tag(int, interval(1, 5))", IntUniformDistribution(1, 5)),
        ("key=tag(log, interval(1, 5))", LogUniformDistribution(1, 5)),
    ],
)
def test_create_optuna_distribution_from_override(input: Any, expected: Any) -> None:
    parser = OverridesParser.create()
    parsed = parser.parse_overrides([input])[0]
    actual = _impl.create_optuna_distribution_from_override(parsed)
    assert expected == actual


def test_create_optuna_distribution_from_override_with_shuffle() -> None:
    parser = OverridesParser.create()
    parsed = parser.parse_overrides(["key=shuffle(range(1,3))"])[0]
    actual = _impl.create_optuna_distribution_from_override(parsed)
    assert isinstance(actual, CategoricalDistribution)
    assert actual.choices == (1, 2) or actual.choices == (2, 1)


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


def test_optuna_example(tmpdir: Path) -> None:
    cmd = [
        "example/sphere.py",
        "--multirun",
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra.sweeper.optuna_config.n_trials=20",
        "hydra.sweeper.optuna_config.n_jobs=8",
        "hydra.sweeper.optuna_config.sampler=RandomSampler",
        "hydra.sweeper.optuna_config.seed=123",
    ]
    get_run_output(cmd)
    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")
    assert isinstance(returns, DictConfig)
    assert returns.name == "optuna"
    assert returns["best_params"]["x"] == 0
    assert returns["best_params"]["y"] == 0
    assert returns["best_value"] == 0
