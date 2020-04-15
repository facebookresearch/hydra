# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from pathlib import Path
from typing import Any

import nevergrad as ng
import pytest  # type: ignore
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root
from omegaconf import DictConfig, OmegaConf

from hydra_plugins.hydra_nevergrad_sweeper import core

chdir_plugin_root()


def test_discovery() -> None:
    assert core.NevergradSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


@pytest.mark.parametrize(  # type: ignore
    "string,param_cls,value_cls",
    [
        ("blu,blublu", ng.p.Choice, str),
        ("0,1,2", ng.p.TransitionChoice, int),
        ("0.0,12.0,2.0", ng.p.Choice, float),
        ("int:1:12", ng.p.Scalar, int),
        ("1:12", ng.p.Scalar, float),
        ("log:0.01:1.0", ng.p.Log, float),
        ("blublu", str, str),
        (
            "Scalar(init=12.1).set_mutation(sigma=3).set_integer_casting()",
            ng.p.Scalar,
            int,
        ),
    ],
)
def test_make_parameter_from_commandline(
    string: str, param_cls: Any, value_cls: Any
) -> None:
    param = core.make_parameter_from_commandline(string)
    assert isinstance(param, param_cls)
    if param_cls is not str:
        assert isinstance(param.value, value_cls)


def test_launched_jobs(sweep_runner: TSweepRunner) -> None:
    budget = 8
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs",
        config_name="compose.yaml",
        task_function=None,
        overrides=[
            "hydra/sweeper=nevergrad",
            "hydra/launcher=basic",
            f"hydra.sweeper.params.optim.budget={budget}",  # small budget to test fast
            "hydra.sweeper.params.optim.num_workers=3",
            "foo=1,2",
            "bar=4:8",
        ],
        strict=True,
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
        f"hydra.sweeper.params.optim.budget={budget}",  # small budget to test fast
        f"hydra.sweeper.params.optim.num_workers={min(8, budget)}",
        "hydra.sweeper.params.optim.seed=12",  # avoid random failures
    ]
    if with_commandline:
        cmd += [
            "db=mnist,cifar",
            "batch_size=4,8,12,16",
            "lr=log:0.001:1.0",
            "dropout=0:1",
        ]
    subprocess.check_call(cmd)
    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")
    assert isinstance(returns, DictConfig)
    assert returns.name == "nevergrad"
    assert len(returns) == 3
    best_parameters = returns.best_parameters
    assert not best_parameters.dropout.is_integer()
    if budget > 1:
        assert best_parameters.batch_size == 4  # this argument should be easy to find
    # check that all job folders are created
    last_job = max(int(fp.name) for fp in Path(tmpdir).iterdir() if fp.name.isdigit())
    assert last_job == budget - 1
