# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import typing as tp
import pytest
import nevergrad as ng
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import TSweepRunner, sweep_runner  # noqa: F401
from hydra_plugins.nevergrad_minimizer import NevergradMinimizer
from hydra_plugins.nevergrad_minimizer.core import make_parameter


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking at the Sweeper plugins
    assert NevergradMinimizer.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


@pytest.mark.parametrize(  # type: ignore
    "string,param_cls,value_cls",
    [("blu,blublu", ng.p.Choice, str),
     ("0,1,2", ng.p.TransitionChoice, int),
     ("0.0,12.0,2.0", ng.p.Choice, float),
     ("1:12", ng.p.Scalar, int),
     ("1.0:12", ng.p.Scalar, float),
     ("blublu", str, str),
     ("Scalar(init=12.1).set_mutation(sigma=3).set_integer_casting()", ng.p.Scalar, int),
     ]
)
def test_make_parameter(
    string: str,
    param_cls: tp.Any,
    value_cls: tp.Any,
) -> None:
    param = make_parameter(string)
    assert isinstance(param, param_cls)
    if param_cls is not str:
        assert isinstance(param.value, value_cls)


def test_launched_jobs(sweep_runner: TSweepRunner) -> None:  # noqa: F811 # type: ignore
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        # TODO: How to give a smaller budget?
        overrides=["hydra/sweeper=nevergrad-minimizer", "hydra/launcher=basic", "foo=1,2"],
        strict=True,
    )
    with sweep:
        assert sweep.returns is not None
        assert len(sweep.returns) == 80
