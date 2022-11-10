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
import logging
from typing import Any, Optional, Sequence, Union

from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.plugins.experiment_sequence import ExperimentSequence
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig

log = logging.getLogger(__name__)


class LokyLauncher(Launcher):
    def __init__(self, **kwargs: Any) -> None:
        """Loky Launcher

        Launches parallel jobs using loky's process pool. For details, refer to:
        https://loky.readthedocs.io/en/stable/API.html#loky.get_reusable_executor

        This plugin is based on the idea and inital implementation of joblib plugin
        """
        self.config: Optional[DictConfig] = None
        self.task_function: Optional[TaskFunction] = None
        self.hydra_context: Optional[HydraContext] = None

        self.loky = kwargs

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.config = config
        self.task_function = task_function
        self.hydra_context = hydra_context

    def launch(
        self, job_overrides: Union[Sequence[Sequence[str]], ExperimentSequence], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        from . import _core

        return _core.launch(
            launcher=self, job_overrides=job_overrides, initial_job_idx=initial_job_idx
        )
