# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from hydra.core.config_store import ConfigStore


@dataclass
class EarlyStopConfig:
    minimize: bool = True

    max_epochs_without_improvement: int = 10

    # An improvement larger than epsilon is considered significant
    epsilon: float = 0.00001


@dataclass
class ExperimentConfig:
    # Experiment name
    name: Optional[str] = None

    # Name of metric to optimize or null if you only return one metric
    objective_name: str = "objective"

    # Defaults to minimize, set to false to maximize
    minimize: bool = True

    # For the remaining paramaters, refer the Ax documentation: https://ax.dev/api/core.html#experiment
    parameter_constraints: Optional[List[str]] = None
    outcome_constraints: Optional[List[str]] = None
    status_quo: Optional[Dict[str, Any]] = None


@dataclass
class ClientConfig:

    verbose_logging: bool = False

    # set random seed here to make Ax results reproducible
    random_seed: Optional[int] = None


@dataclass
class AxConfig:

    # max_trials is application-specific. Tune it for your use case
    max_trials: int = 10
    early_stop: EarlyStopConfig = EarlyStopConfig()
    experiment: ExperimentConfig = ExperimentConfig()
    client: ClientConfig = ClientConfig()
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AxSweeperConf:
    _target_: str = "hydra_plugins.hydra_ax_sweeper.ax_sweeper.AxSweeper"
    # Maximum number of trials to run in parallel
    max_batch_size: Optional[int] = None
    ax_config: AxConfig = AxConfig()


ConfigStore.instance().store(
    group="hydra/sweeper", name="ax", node=AxSweeperConf, provider="ax_sweeper"
)
