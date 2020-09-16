# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from pathlib import Path
from typing import Any

import nevergrad as ng
import pytest
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root
from omegaconf import DictConfig, OmegaConf

from hydra_plugins.hydra_nevergrad_sweeper import core
from hydra_plugins.hydra_nevergrad_sweeper.nevergrad_sweeper import NevergradSweeper

chdir_plugin_root()


def test_discovery() -> None:
    assert NevergradSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


@pytest.mark.parametrize(  # type: ignore
    "params,param_cls, param_val",
    [
        ([1, 2, 3], ng.p.Choice, {1, 2, 3}),
        (["1", "2", "3"], ng.p.Choice, {"1", "2", "3"}),
        ({"lower": 1, "upper": 12, "log": True}, ng.p.Log, ([1.0], [12.0])),
        ({"lower": 1, "upper": 12}, ng.p.Scalar, ([1.0], [12.0])),
        ({"lower": 1, "upper": 12, "integer": True}, ng.p.Scalar, ([1], [12])),
        (
            {"lower": 1, "upper": 12, "log": True, "integer": True},
            ng.p.Log,
            ([1], [12]),
        ),
    ],
)
def test_create_nevergrad_parameter_from_config(
    params: str, param_cls: Any, param_val: Any
) -> None:
    param = core.create_nevergrad_parameter(params)
    verify_param(param, param_cls, param_val)


@pytest.mark.parametrize(  # type: ignore
    "override,param_cls, param_val",
    [
        ("key=choice(1,2)", ng.p.Choice, {1, 2}),
        ("key=choice('hello','world')", ng.p.Choice, {"hello", "world"}),
        ("key=tag(ordered, choice(1,2,3))", ng.p.TransitionChoice, {1, 2, 3}),
        (
            "key=tag(ordered, choice('hello','world', 'nevergrad'))",
            ng.p.TransitionChoice,
            {"hello", "world", "nevergrad"},
        ),
        ("key=range(1,3)", ng.p.Choice, {1, 2}),
        ("key=shuffle(range(1,3))", ng.p.Choice, {1, 2}),
        ("key=range(1,8)", ng.p.Scalar, ([1], [8])),
        ("key=float(range(1,8))", ng.p.Scalar, ([1.0], [8.0])),
        ("key=interval(1,12)", ng.p.Scalar, ([1.0], [12.0])),
        ("key=int(interval(1,12))", ng.p.Scalar, ([1], [12])),
        ("key=tag(log, interval(1,12))", ng.p.Log, ([1.0], [12.0])),
        ("key=tag(log, int(interval(1,12)))", ng.p.Log, ([1], [12])),
    ],
)
def test_create_nevergrad_parameter_from_override(
    override: str, param_cls: Any, param_val: Any
) -> None:
    parser = OverridesParser.create()
    parsed = parser.parse_overrides([override])[0]
    param = core.create_nevergrad_parameter(parsed)
    verify_param(param, param_cls, param_val)


def verify_param(output_param: Any, expected_param_cls: Any, param_val: Any) -> None:
    assert isinstance(output_param, expected_param_cls)
    if isinstance(output_param, ng.p.Choice):
        assert set(output_param.choices.value) == param_val
    elif isinstance(output_param, ng.p.Scalar):
        if output_param.integer:
            actual = (
                list(map(int, output_param.bounds[0])),  # type: ignore
                list(map(int, output_param.bounds[1])),  # type: ignore
            )
        else:
            actual = (
                list(map(lambda x: float(x), output_param.bounds[0])),  # type: ignore
                list(map(lambda x: float(x), output_param.bounds[1])),  # type: ignore
            )
        assert actual == param_val and isinstance(actual[0][0], type(param_val[0][0]))


def test_launched_jobs(hydra_sweep_runner: TSweepRunner) -> None:
    budget = 8
    sweep = hydra_sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs",
        config_name="compose.yaml",
        task_function=None,
        overrides=[
            "hydra/sweeper=nevergrad",
            "hydra/launcher=basic",
            f"hydra.sweeper.optim.budget={budget}",  # small budget to test fast
            "hydra.sweeper.optim.num_workers=3",
            "foo=1,2",
            "bar=4:8",
        ],
    )
    with sweep:
        assert sweep.returns is None


@pytest.mark.parametrize("with_commandline", (True, False))  # type: ignore
def test_nevergrad_example(with_commandline: bool, tmpdir: Path) -> None:
    budget = 32 if with_commandline else 1  # make a full test only once (faster)
    cmd = [
        sys.executable,
        "example/dummy_training.py",
        "-m",
        "hydra.sweep.dir=" + str(tmpdir),
        f"hydra.sweeper.optim.budget={budget}",  # small budget to test fast
        f"hydra.sweeper.optim.num_workers={min(8, budget)}",
        "hydra.sweeper.optim.seed=12",  # avoid random failures
    ]
    if with_commandline:
        cmd += [
            "db=mnist,cifar",
            "batch_size=4,8,12,16",
            "lr=tag(log, interval(0.001, 1.0))",
            "dropout=interval(0,1)",
        ]
    subprocess.check_call(cmd)
    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")
    assert isinstance(returns, DictConfig)
    assert returns.name == "nevergrad"
    assert len(returns) == 3
    best_parameters = returns.best_evaluated_params
    assert not best_parameters.dropout.is_integer()
    if budget > 1:
        assert best_parameters.batch_size == 4  # this argument should be easy to find
    # check that all job folders are created
    last_job = max(int(fp.name) for fp in Path(tmpdir).iterdir() if fp.name.isdigit())
    assert last_job == budget - 1
