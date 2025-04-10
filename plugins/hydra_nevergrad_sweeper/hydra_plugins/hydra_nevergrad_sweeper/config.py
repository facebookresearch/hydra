# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List, Tuple, TypeAlias, Union, Callable
from pathlib import Path

from hydra.core.config_store import ConfigStore


CheapConstraintFn: TypeAlias = Any
"""A cheap function that can be used to prune bad candidates early.
See https://facebookresearch.github.io/nevergrad/\
    optimization.html#optimization-with-constraints for more details.
Actual type: Callable[[Dict[str, Any]], Union[bool, float]]
"""


@dataclass
class ScalarOrArrayConfigSpec:
    """Representation of all the options to define
    a scalar.
    """

    # lower bound if any
    lower: Optional[float | List[float]] = None

    # upper bound if any
    upper: Optional[float | List[float]] = None

    # initial value
    # default to the middle point if completely bounded
    # ng.p.Array used if init is set
    init: Optional[float | List[float]] = None

    # step size for an update
    # defaults to 1 if unbounded
    # or 1/6 of the range if completely bounded
    step: Optional[float | List[float]] = None

    # cast to integer
    integer: bool = False

    # logarithmically distributed
    # unused for array types
    log: bool = False

    # shape of the array
    # if set, ng.p.Array is used
    shape: Optional[Tuple[int]] = None


@dataclass
class CallbackConfigSpec:
    """Representation of all the options to define a callback."""

    # name of the callback. either "ask" or "tell"
    name: str

    # callback function
    # Actual type: Callable[[ng.optimizers.base.Optimizers], None]
    callback: Any


@dataclass
class OptimConf:
    # name of the Nevergrad optimizer to use. Here is a sample:
    #   - "OnePlusOne" extremely simple and robust, especially at low budget, but
    #     tends to converge early.
    #   - "CMA" very good algorithm, but may require a significant budget (> 120)
    #   - "TwoPointsDE": an algorithm good in a wide range of settings, for significant
    #     budgets (> 120).
    #   - "NGOpt" an algorithm aiming at identifying the best optimizer given your input
    #     definition (updated regularly)
    # find out more within nevergrad's documentation:
    # https://github.com/facebookresearch/nevergrad/
    optimizer: str = "NGOpt"

    # total number of function evaluations to perform
    budget: int = 80

    # number of parallel workers for performing function evaluations
    num_workers: int = 10

    # set to true if the function evaluations are noisy
    noisy: bool = False

    # set to true for performing maximization instead of minimization
    maximize: bool = False

    # optimization seed, for reproducibility
    seed: Optional[int] = None

    # maximum authorized failure rate for a batch of parameters
    max_failure_rate: float = 0.0

    # Define cheap constraints configuration via Python methods.
    # If given, `cheap_constraints` should be a dict of callables with the signature
    # Callable[[Dict[str, Any]], float | bool]. The input dict is the parameterization
    # of the trial.
    # https://facebookresearch.github.io/nevergrad/optimization.html#optimization-with-constraints
    cheap_constraints: Dict[str, CheapConstraintFn] = field(default_factory=dict)

    # These are callbacks that are passed to the optimizer via the `register_callback`
    # method. See the Nevergrad documentation for more information.
    # https://facebookresearch.github.io/nevergrad/optimizers_ref.html#nevergrad.optimizers.base.Optimizer.register_callback
    callbacks: Dict[str, CallbackConfigSpec] = field(default_factory=dict)

    # Load an existing study and resume it. This is the path to the saved optimizer
    # pickle. You can pickle the optimizer via the OptimizerDump callback.
    load_if_exists: Optional[Path] = None


@dataclass
class NevergradSweeperConf:
    _target_: str = (
        "hydra_plugins.hydra_nevergrad_sweeper.nevergrad_sweeper.NevergradSweeper"
    )

    # configuration of the optimizer
    optim: OptimConf = field(default_factory=OptimConf)

    # default parametrization of the search space
    # can be specified:
    # - as a string, like commandline arguments
    # - as a list, for categorical variables
    # - as a full scalar specification
    parametrization: Dict[str, Any] = field(default_factory=dict)


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="nevergrad",
    node=NevergradSweeperConf,
    provider="nevergrad",
)
