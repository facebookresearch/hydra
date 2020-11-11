# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from typing import Any

from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root, get_run_output
import pytest
from optuna.distributions import (
    CategoricalDistribution,
    IntLogUniformDistribution,
    IntUniformDistribution,
    LogUniformDistribution,
    UniformDistribution
)
from omegaconf import DictConfig, OmegaConf


from hydra_plugins.hydra_optuna_sweeper import _impl
from hydra_plugins.hydra_optuna_sweeper.optuna_sweeper import OptunaSweeper

chdir_plugin_root()


def test_discovery() -> None:
    assert OptunaSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


def assert_optuna_distribution_equals(expected: Any, actual: Any) -> None:
    assert type(expected) == type(actual)
    if isinstance(actual, CategoricalDistribution):
        assert sorted(expected.choices) == sorted(actual.choices)
    elif isinstance(actual, (IntLogUniformDistribution, LogUniformDistribution)):
        assert expected.low == actual.low
        assert expected.high == actual.high
    elif isinstance(actual, (IntUniformDistribution, UniformDistribution)):
        assert expected.low == actual.low
        assert expected.high == actual.high
        if isinstance(actual, IntUniformDistribution):
            assert expected.step == actual.step
    else:
        assert False, f"Unexpected type: {type(actual)}"


@pytest.mark.parametrize(  # type: ignore
    "input, expected",
    [
        ({"type": "choice", "values": [1, 2, 3]}, CategoricalDistribution([1, 2, 3])),
        ({"type": "range", "values": [0, 10]}, IntUniformDistribution(0, 10)),
        ({"type": "range", "values": [0, 10], "step": 2}, IntUniformDistribution(0, 10, step=2)),
        ({"type": "interval", "values": [0, 1]}, UniformDistribution(0, 1)),
        ({"type": "interval", "values": [0, 5], "tags": ["int"]}, IntUniformDistribution(0, 5)),
        ({"type": "interval", "values": [1, 100], "log": True}, LogUniformDistribution(1, 100)),
        ({"type": "interval", "values": [1, 100], "tags": ["int"], "log": True}, IntLogUniformDistribution(1, 100)),
    ]
)
def test_create_optuna_distribution_from_config(input: Any, expected: Any) -> None:
    actual = _impl.create_optuna_distribution_from_config(input)
    assert_optuna_distribution_equals(expected, actual)


@pytest.mark.parametrize(  # type: ignore
    "input, expected",
    [
        ("key=choice(1,2)", CategoricalDistribution([1, 2])),
        ("key=choice('hello', 'world')", CategoricalDistribution(["hello", "world"])),
        ("key=range(1,3)", IntUniformDistribution(1, 3)),
        ("key=shuffle(range(1,3))", CategoricalDistribution([1, 2])),
        ("key=interval(1, 5)", UniformDistribution(1, 5)),
        ("key=tag(int, interval(1, 5))", IntUniformDistribution(1, 5)),
        ("key=tag(log, interval(1, 5))", LogUniformDistribution(1, 5)),
    ]
)
def test_create_optuna_distribution_from_override(input: Any, expected: Any) -> None:
    parser = OverridesParser.create()
    parsed = parser.parse_overrides([input])[0]
    dist = _impl.create_optuna_distribution_from_override(parsed)
    assert_optuna_distribution_equals(expected, dist)


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
        ]
    )
    with sweep:
        assert sweep.returns is None


def test_optuna_example(tmpdir: Path):
    cmd = [
        "example/sphere.py",
        "-m",
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra.sweeper.optuna_config.n_trials=20",
        "hydra.sweeper.optuna_config.n_jobs=8",
    ]
    get_run_output(cmd)
    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")
    assert isinstance(returns, DictConfig)
    assert returns.name == "optuna"
    assert "best_params" in returns
    assert "best_value" in returns

