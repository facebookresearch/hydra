from dataclasses import dataclass, field
from typing import Any, Dict, MutableSequence, Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, DictConfig, ListConfig


@dataclass
class WandbParameterSpec:
    """Representation of all the options to define
    a Wandb parameter.
    """

    # (int or float) Maximum and minimum values.
    # if int, for int uniform-distributed hyperparameters. If float, for uniform-distributed hyperparameters.
    min: Optional[float] = None
    max: Optional[float] = None

    # (float) Mean parameter for normal or log normal-distributed hyperparameters.
    mu: Optional[float] = 0

    # (float) Standard deviation parameter for normal or log normal-distributed hyperparameters.
    sigma: Optional[float] = 1

    # (float) Quantization step size for quantized hyperparameters.
    q: Optional[float] = 1

    # Specify how values will be distributed
    # Supported distributions and required parameters
    # "constant": ["value"],
    # "categorical": ["values"],
    # "int_uniform": ["min", "max"],
    # "uniform": ["min", "max"],
    # "q_uniform": ["min", "max", "q"],
    # "log_uniform": ["min", "max"],
    # "q_log_uniform": ["min", "max", "q"],
    # "inv_log_uniform": ["min", "max"],
    # "normal": ["mu", "sigma"],
    # "q_normal": ["mu", "sigma", "q"],
    # "log_normal": ["mu", "sigma"],
    # "q_log_normal": ["mu", "sigma", "q"],
    distribution: Optional[str] = None
    value: Optional[float] = None
    values: Optional[MutableSequence] = None


@dataclass
class WandbConfig:
    # (Required) The name of the sweep, displayed in the W&B UI.
    name: str = MISSING

    # (Required) The hyperparam sweep search strategy.
    method: str = MISSING

    # Number of function evaluations to perform per agent
    count: Optional[int] = 1

    # Specify the metric to optimize (only used by certain search strategies and stopping criteria).
    metric: Optional[DictConfig] = DictConfig({})

    # Number of agents to launch in a batch until budget is reached
    num_agents: Optional[int] = 1

    # Can provide a sweep ID from a pre-existing sweep if you wanted to continue from it
    sweep_id: Optional[str] = None

    # The entity for this sweep. Otherwise infer from the environment.
    entity: Optional[str] = None

    # Specify the project this sweep will be under. Projects are used to
    # organize models that can be compared, working on the same problem
    # with different architectures, hyperparameters, datasets, preprocessing etc.
    project: Optional[str] = None

    # Wandb early termination. Check wandb.yaml in /example for an example config
    early_terminate: Optional[DictConfig] = DictConfig({})

    # Tags can be used to label runs from an agent with particular features, such as
    # the runs being pre-emptible. It's all up to the user to fill this out.
    tags: Optional[ListConfig] = ListConfig([])

    # Total number of agents to launch
    budget: Optional[int] = 1

    # Notes can contain a string, a list, or any OmegaConf type (e.g., if you wanted to pass a config value
    # that interoplated into a ListConfig, like ${hydra.overrides.task})
    notes: Optional[Any] = None

    # Maximum authorized failure rate for a batch of wandb agents' runs (since each agent can execute >= 1 runs)
    max_run_failure_rate: float = 0.0

    # Maximum authorized failure rate for a batch of wandb agents launched by the launcher
    max_agent_failure_rate: float = 0.0


@dataclass
class WandbSweeperConf:
    wandb_sweep_config: WandbConfig = WandbConfig()
    _target_: str = "hydra_plugins.hydra_wandb_sweeper.wandb_sweeper.WandbSweeper"

    # Parametrization of the wandb sweep search space can be specified:
    # - as a string, like commandline arguments
    # - as a list, for categorical variables
    # - as a full scalar specification
    params: Dict[str, Any] = field(default_factory=dict)


ConfigStore.instance().store(
    group="hydra/sweeper", name="wandb", node=WandbSweeperConf, provider="wandb_sweeper"
)
