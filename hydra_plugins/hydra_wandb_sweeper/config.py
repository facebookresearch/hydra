import dataclasses
import typing

import omegaconf
from hydra.core import config_store


@dataclasses.dataclass
class WandbConfig:
    name: str
    method: str
    count: typing.Optional[int] = None
    metric: typing.Optional[omegaconf.DictConfig] = omegaconf.DictConfig({})
    num_agents: typing.Optional[int] = 1
    sweep_id: typing.Optional[str] = None
    entity: typing.Optional[str] = None
    project: typing.Optional[str] = None
    early_terminate: typing.Optional[omegaconf.DictConfig] = omegaconf.DictConfig({})
    preemptible: typing.Optional[bool] = False


@dataclasses.dataclass
class WandbSweeperConf:
    wandb_sweep_config: WandbConfig
    _target_: str = "hydra_plugins.hydra_wandb_sweeper.wandb_sweeper.WandbSweeper"


config_store.ConfigStore.instance().store(
    group="hydra/sweeper", name="wandb", node=WandbSweeperConf, provider="wandb_sweeper"
)
