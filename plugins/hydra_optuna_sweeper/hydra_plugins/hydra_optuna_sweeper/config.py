# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from hydra.core.config_store import ConfigStore


@dataclass
class ParamConfig:
    type: str
    values: List[Union[str, int, float]]
    log: bool = False
    step: float = 1
    tags: Optional[List[str]] = None


@dataclass
class OptunaConfig:

    # Direction of optimization
    # "minimize" or "maximize"
    direction: str = "minimize"

    # Storage URL to persist optimization results
    storage: Optional[str] = None

    # Name of study to persist optimization results
    study_name: Optional[str] = None

    # Total number of function evaluations
    n_trials: int = 20

    # Number of parallel workers
    n_jobs: int = 2

    # Sampling algorithm such as RandomSampler, TPESampler and CmaEsSampler
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
