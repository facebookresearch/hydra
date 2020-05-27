# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from hydra.core.config_store import ConfigStore
from hydra.types import ObjectConf


@dataclass
class ScalarConfigSpec:
    """Representation of all the options to define
    a scalar.
    """

    # lower bound if any
    lower: Optional[float] = None

    # upper bound if any
    upper: Optional[float] = None

    # initial value
    # default to the middle point if completely bounded
    init: Optional[float] = None

    # step size for an update
    # defaults to 1 if unbounded
    # or 1/6 of the range if completely bounderd
    step: Optional[float] = None

    # cast to integer
    integer: bool = False

    # logarithmically distributed
    log: bool = False


@dataclass
class OptimConf:

    # name of the Nevergrad optimizer to use. Here is a sample:
    #   - "OnePlusOne" extremely simple and robust, especially at low budget, but
    #     tends to converge early.
    #   - "CMA" very good algorithm, but may require a significant budget (> 120)
    #   - "TwoPointsDE": an algorithm good in a wide range of settings, for significant
    #     budgets (> 120).
    #   - "Shiwa" an algorithm aiming at identifying the best optimizer given your input
    #     definition (work in progress, it may still be ill-suited for low budget)
    # find out more within nevergrad's documentation:
    # https://github.com/facebookresearch/nevergrad/
    optimizer: str = "OnePlusOne"

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


@dataclass
class NevergradConf:

    # configuration of the optimizer
    optim: OptimConf = OptimConf()

    # default parametrization of the search space
    # can be specified:
    # - as a string, like commandline arguments
    # - as a list, for categorical variables
    # - as a full scalar specification
    parametrization: Dict[str, Any] = field(default_factory=dict)

    # version of the commandline API
    version: int = 1


@dataclass
class NevergradSweeperConf(ObjectConf):
    cls: str = "hydra_plugins.hydra_nevergrad_sweeper.core.NevergradSweeper"
    params: NevergradConf = NevergradConf()


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="nevergrad",
    node=NevergradSweeperConf,
    provider="nevergrad",
)
