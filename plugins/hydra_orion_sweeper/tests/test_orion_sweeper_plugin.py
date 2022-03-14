# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys
from copy import deepcopy
from pathlib import Path

from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.test_utils import (
    TSweepRunner,
    chdir_plugin_root,
    run_process,
    run_python_script,
)
from omegaconf import DictConfig, OmegaConf
from pytest import mark

from hydra_plugins.hydra_orion_sweeper import _impl
from hydra_plugins.hydra_orion_sweeper.orion_sweeper import OrionSweeper

chdir_plugin_root()

parametrization = dict(
    a0="uniform(0, 1)",
    a01="uniform(3, 4, discrete=True)",
    a02="choices([4, 6])",
    a1="uniform(0, 1, discrete=True)",
    a2="uniform(0, 1, precision=2)",
    b0="loguniform(1, 2)",
    b1="loguniform(1, 2, discrete=True)",
    b2="loguniform(1, 2, precision=2)",
    c0="normal(0, 1)",
    c1="normal(0, 1, discrete=True)",
    c2="normal(0, 1, precision=True)",
    d0="choices(['a', 'b'])",
    e0="fidelity(10, 100)",
    e1="fidelity(10, 100, base=3)",
    r1=123,
)

nevergrad_overrides = [
    "a0=interval(1, 2)",
    "a01=range(1, 2)",
    "a02=range(4, 8, 2)",
    "a1=int(interval(1, 2))",
    "b0=tag(log, interval(0.001, 1.0))",
    "d0=a,b,c,d",
    "r1=234",
    # Nevergrad does not have an equivalent
    'e1="fidelity(2, 10, base=4)"',
    'c0="normal(2, 10)"',
]

orion_overrides = [
    'a0="uniform(1, 2)"',
    'a01="uniform(1, 2, discrete=True)"',
    'a02="choices([4, 6, 8])"',
    'a1="uniform(1, 2, discrete=True)"',
    'b0="loguniform(0.001, 1.0)"',
    "d0=\"choices(['a', 'b', 'c', 'd'])\"",
    'e1="fidelity(2, 10, base=4)"',
    'c0="normal(2, 10)"',
    "r1=234",
]

overriden_parametrization = dict(
    a0="uniform(1, 2)",
    a01="uniform(1, 2, discrete=True)",
    a02="choices([4, 6, 8])",
    a1="uniform(1, 2, discrete=True)",
    b0="loguniform(0.001, 1.0)",
    d0="choices(['a', 'b', 'c', 'd'])",
    e1="fidelity(2, 10, base=4)",
    c0="normal(2, 10)",
)


def test_discovery() -> None:
    assert OrionSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


@mark.parametrize("overrides", ([], orion_overrides, nevergrad_overrides))
def test_space_parser(overrides):
    space_params = deepcopy(parametrization)
    space_params.pop("r1")

    parser = _impl.SpaceParser()
    parser.add_from_parametrization(parametrization)

    space, args = parser.space()
    assert space.configuration == space_params, "Generated space match definition"
    assert args == dict(r1=123), "Regular argument was identified"

    if len(overrides) > 0:
        parser.add_from_overrides(overrides)
        space, args = parser.space()

        space_params.update(overriden_parametrization)

        assert (
            space.configuration == space_params
        ), "Generated space match overriden definition"
        assert args == dict(r1=234), "Regular argument was overriden"


orion_functions_overrides = [
    "a0=uniform(1, 2)",
    "a01=uniform(1, 2, discrete=True)",
    "a02=choices([4, 6, 8])",
    "a1=uniform(1, 2, discrete=True)",
    "b0=loguniform(0.001, 1.0)",
    "d0=choices(['a', 'b', 'c', 'd'])",
    "e1=fidelity(2, 10, base=4)",
    "c0=normal(2, 10)",
]


def test_override_parser():
    parser = _impl.override_parser()
    parsed = parser.parse_overrides(orion_functions_overrides)

    for override in parsed:
        values = override.value()
        name = override.get_key_element()

        target = overriden_parametrization.get(name)

        assert isinstance(values, _impl.SpaceFunction)
        dim = values(name)

        assert dim.get_prior_string() == target


def test_launched_jobs(hydra_sweep_runner: TSweepRunner) -> None:
    budget = 8
    sweep = hydra_sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs",
        config_name="compose.yaml",
        task_function=None,
        overrides=[
            "hydra/sweeper=orion",
            "hydra/launcher=basic",
            f"hydra.sweeper.worker.max_trials={budget}",  # small budget to test fast
            "hydra.sweeper.worker.n_workers=3",
            "foo='choices([1, 2])'",
            "bar='choices([4, 5, 6, 7, 8])'",
        ],
    )

    with sweep:
        assert sweep.returns is None


@mark.parametrize("with_commandline, with_orion_format", [(True, False), (True, False)])
def test_orion_example(
    with_commandline: bool, with_orion_format: bool, tmpdir: Path
) -> None:
    budget = 32 if with_commandline else 1  # make a full test only once (faster)

    cmd = [
        "example/my_app.py",
        "-m",
        "hydra.sweep.dir=" + str(tmpdir),
        "hydra.job.chdir=True",
        f"hydra.sweeper.worker.max_trials={budget}",  # small budget to test fast
        f"hydra.sweeper.worker.n_workers={min(8, budget)}",
    ]

    if with_commandline:
        if with_orion_format:
            cmd += [
                "opt='\"choices(['Adam', 'SGD'])\"'",
                "batch_size='\"choices([4,8,12,16])\"'",
                "lr='\"loguniform(0.001, 1.0)\"'",
                "dropout=uniform(0,1)",
            ]
        else:
            cmd += [
                "opt=Adam,SGD",
                "batch_size=4,8,12,16",
                "lr=tag(log, interval(0.001, 1.0))",
                "dropout=interval(0,1)",
            ]

    run_python_script(cmd)

    returns = OmegaConf.load(f"{tmpdir}/optimization_results.yaml")

    assert isinstance(returns, DictConfig)
    assert returns.name == "orion"
    assert len(returns) == 8

    best_parameters = returns.best_evaluated_params
    assert not best_parameters.dropout.is_integer()

    if budget > 1:
        assert best_parameters.batch_size == 4  # this argument should be easy to find

    # check that all job folders are created
    last_job = max(int(fp.name) for fp in Path(tmpdir).iterdir() if fp.name.isdigit())
    assert last_job == budget - 1


def test_failure_rate(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "example/my_app.py",
        "-m",
        f"hydra.sweep.dir={tmpdir}",
        "hydra.sweeper.worker.max_trials=2",  # small budget to test fast
        "hydra.sweeper.worker.n_workers=2",
        f"hydra.sweeper.worker.max_broken=1",
        "error=true",
    ]

    _, err = run_process(cmd, print_error=False, raise_exception=False)

    original_error_string = "RuntimeError: cfg.error is True"
    assert original_error_string in err

    broken_error_string = "BrokenExperiment: Max broken trials reached, stopping"
    assert broken_error_string in err


formats = ("float", "list", "dict", "none")


@mark.parametrize("format", formats)
def test_return_format(format: str, tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "example/my_app.py",
        "-m",
        f"hydra.sweep.dir={tmpdir}",
        "hydra.sweeper.worker.max_trials=2",  # small budget to test fast
        "hydra.sweeper.worker.n_workers=2",
        f"hydra.sweeper.worker.max_broken=1",
        f"return_type={format}",
    ]

    _, err = run_process(cmd, print_error=False, raise_exception=False)

    if format == "none":
        format_error = "InvalidResult: Value 'None' of type '<class 'NoneType'>' is not an expected return type"
        broken_error_string = "BrokenExperiment: Max broken trials reached, stopping"

        assert format_error in err
        assert broken_error_string in err
