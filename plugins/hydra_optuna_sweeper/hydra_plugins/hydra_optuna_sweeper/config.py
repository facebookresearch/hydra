# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from hydra.core.config_store import ConfigStore


class Direction(Enum):
    minimize = 1
    maximize = 2


@dataclass
class DistributionConfig:

    # Type of distribution. "int", "float" or "categorical"
    type: str

    # Choices of categorical distribution
    choices: Optional[List[Union[str, int, float]]] = None

    # Lower bound of int or float distribution
    low: Optional[float] = None

    # Upper bound of int or float distribution
    high: Optional[float] = None

    # If True, space is converted to the log domain
    # Valid for int or float distribution
    log: bool = False

    # Discritization step
    # Valid for int or float distribution
    step: float = 1


@dataclass
class OptunaConfig:

    # Direction of optimization
    direction: Direction = Direction.minimize

    # Storage URL to persist optimization results
    storage: Optional[str] = None

    # Name of study to persist optimization results
    study_name: Optional[str] = None

    # Total number of function evaluations
    n_trials: int = 20

    # Number of parallel workers
    n_jobs: int = 2

    # Sampling algorithm such as RandomSampler, TPESampler and CmaEsSampler
    # Please refer to the reference for further details
    # https://optuna.readthedocs.io/en/stable/reference/samplers.html
    sampler: Optional[str] = None

    # Random seed of sampler
    seed: Optional[int] = None


@dataclass
class OptunaSweeperConf:
    _target_: str = "hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper"

    optuna_config: OptunaConfig = OptunaConfig()

    search_space: Dict[str, Any] = field(default_factory=dict)


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="optuna",
    node=OptunaSweeperConf,
    provider="optuna_sweeper",
)
