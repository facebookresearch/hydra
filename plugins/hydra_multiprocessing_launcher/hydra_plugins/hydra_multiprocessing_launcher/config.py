# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Optional

from hydra.core.config_store import ConfigStore


@dataclass
class MultiprocessingLauncherConf:
    _target_: str = "hydra_plugins.hydra_multiprocessing_launcher.multiprocessing_launcher.MultiprocessingLauncher"

    # maximum number of concurrently running jobs. if None, all CPUs are used
    processes: Optional[int] = None

    # the number of tasks a worker process can complete before it will exit and be replaced with a fresh worker process
    maxtasksperchild: Optional[int] = None


ConfigStore.instance().store(
    group="hydra/launcher",
    name="multiprocessing",
    node=MultiprocessingLauncherConf,
    provider="multiprocessing_launcher",
)
