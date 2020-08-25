# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from pathlib import Path
from typing import Any

import nevergrad as ng

import pytest  # type: ignore
from hydra.core.override_parser.types import Override
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root
from omegaconf import DictConfig, OmegaConf

from hydra_plugins.hydra_nevergrad_sweeper import core
from tests import get_choice_sweep, get_override_element, get_range_sweep

chdir_plugin_root()


def test_discovery() -> None:
    assert core.NevergradSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


@pytest.mark.parametrize(  # type: ignore
    "override,param_cls,value_cls",
    [
        (get_choice_sweep(["blu", "blublu"]), ng.p.Choice, str),
        (get_choice_sweep([0, 1, 2]), ng.p.TransitionChoice, int),
        (get_choice_sweep(["0", "1", "2"]), ng.p.Choice, str),
        (get_choice_sweep([0.0, 12.0, 2.0]), ng.p.Choice, float),
        (get_range_sweep(start=1.0, stop=12.0), ng.p.Scalar, float),
        (get_range_sweep(start=1, stop=12), ng.p.Scalar, int),
        (get_range_sweep(tags={"log"}, start=0.01, stop=1.0), ng.p.Log, float),
        (get_override_element("blublu"), str, str),
    ],
)
def test_make_nevergrad_parameter(
    override: Override, param_cls: Any, value_cls: Any
) -> None:
    param = core.make_nevergrad_parameter(override)
    assert isinstance(param, param_cls)
    if param_cls is not str:
        assert isinstance(param.value, value_cls)


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
            "db=choice(mnist,cifar)",
            "batch_size=choice(4,8,12,16)",
            "lr=tag(log, range(0.001, 1.0))",
            "dropout=float(range(0,1))",
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
