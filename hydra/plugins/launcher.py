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
"""
Launcher plugin interface
"""
from abc import abstractmethod
from typing import Sequence

from omegaconf import DictConfig

from hydra.core.utils import JobReturn
from hydra.plugins.experiment_sequence import ExperimentSequence
from hydra.types import TaskFunction, HydraContext

from .plugin import Plugin


class Launcher(Plugin):
    @abstractmethod
    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        """
        Sets this launcher instance up.
        """
        raise NotImplementedError()

    @abstractmethod
    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        """
        :param job_overrides: a batch of job arguments
        :param initial_job_idx: Initial job idx. used by sweepers that executes several batches
        """
        raise NotImplementedError()
    
    def launch_experiment_sequence(
        self, job_overrides: ExperimentSequence, initial_job_idx: int
    ) -> Sequence[JobReturn]:
        """
        :param job_overrides: a batch of job arguments
        :param initial_job_idx: Initial job idx. used by sweepers that executes several batches
        """
        raise NotImplementedError(
            "This launcher doesn't support launching experiment sequence."
        )
