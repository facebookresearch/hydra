# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from hydra.core.config_store import ConfigStore


@dataclass
class OrionClientConf:
    """Orion EVC options"""

    name: Optional[str] = None
    version: Optional[str] = None
    branching: Optional[str] = None
    debug: Optional[str] = False


@dataclass
class WorkerConf:
    """Orion Worker configuration"""

    n_workers: int = 1
    pool_size: Optional[int] = None
    reservation_timeout: int = 120
    max_trials: int = 10000000
    max_trials_per_worker: int = 1000000
    max_broken: int = 3


@dataclass
class StorageConf:
    """Orion storage configuration"""

    type: str = "pickledb"
    host: str = "orion_database.pkl"


@dataclass
class AlgorithmConf:
    """Orion optimization algorithm configuration"""

    type: str = "random"
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrionSweeperConf:
    _target_: str = "hydra_plugins.hydra_orion_sweeper.orion_sweeper.OrionSweeper"

    orion: OrionClientConf = OrionClientConf()

    worker: WorkerConf = WorkerConf()

    algorithm: AlgorithmConf = AlgorithmConf()

    storage: StorageConf = StorageConf()

    # default parametrization of the search space
    parametrization: Dict[str, Any] = field(default_factory=dict)


ConfigStore.instance().store(
    group="hydra/sweeper",
    name="orion",
    node=OrionSweeperConf,
    provider="orion",
)
