# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Optional

from hydra.core.config_store import ConfigStore
from hydra.types import ObjectConf

# finally, register two different choices:
ConfigStore.instance().store(
    group="hydra/launcher",
    name="tsp",
    node=ObjectConf(
        cls="hydra_plugins.hydra_tsp_launcher.tsp_launcher.TaskSpoolerLauncher",
        params={},
    ),
    provider="tsp_launcher",
)