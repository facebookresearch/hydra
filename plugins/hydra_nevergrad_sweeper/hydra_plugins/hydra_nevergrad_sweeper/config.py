# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Any, Optional

from hydra.core.config_store import ConfigStore
from hydra.types import ObjectConf


@dataclass
class NevergradOptimConf:

    # name of the Nevergrad optimizer to use. Here is a sample:
    #   - "OnePlusOne" extremely simple and robust, especially at low budget, but
    #     tends to converge early.
    #   - "CMA" very good algorithm, but may require a significant budget (> 120)
    #   - "TwoPointsDE": an algorithm good in a wide range of settings, for significant
    #     budgets (> 120).
    #   - "Shiva" an algorithm aiming at identifying the best optimizer given your input
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
class NevergradFullConf:

    # configuration of the optimizer
    optim: NevergradOptimConf = NevergradOptimConf()

    # default parametrization of the search space
    parametrization: Any = None

    # version of the commandline API
    version: int = 1


@dataclass
class NevergradSweeperConf(ObjectConf):
    cls: str = "hydra_plugins.hydra_nevergrad_sweeper.core.NevergradSweeper"
    params: NevergradFullConf = NevergradFullConf()


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="nevergrad",
    path="hydra.sweeper",
    node=NevergradSweeperConf,
)
