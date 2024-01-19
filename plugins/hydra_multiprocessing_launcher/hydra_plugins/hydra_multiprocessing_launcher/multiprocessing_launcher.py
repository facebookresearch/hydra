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
import multiprocessing as mp
import multiprocessing.pool

from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.plugins.experiment_sequence import ExperimentSequence
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig

log = logging.getLogger(__name__)


class NoDaemonProcess(mp.context.SpawnProcess):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(mp.context.BaseContext):
    _name = 'spawn'
    Process = NoDaemonProcess


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class NestablePool(mp.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs['context'] = NoDaemonContext()
        super(NestablePool, self).__init__(*args, **kwargs)


class MultiprocessingLauncher(Launcher):
    def __init__(self, **kwargs: Any) -> None:
        """Multiprocessing Launcher

        Launches parallel jobs using modified multiprocessing process pool. For details, refer to:
        https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
        and https://stackoverflow.com/questions/6974695/python-process-pool-non-daemonic

        Custom NestablePool is created to allow spawned jobs to create own threads (ex. multi-worker DataLoaders)
        WARNING: NestablePool uses non daemonic processes, resouce menagement is on the user side. 
                 We recomend setting `maxtasksperchild=1`

        This plugin is based on the idea and inital implementation of joblib launcher.
        """
        self.config: Optional[DictConfig] = None
        self.task_function: Optional[TaskFunction] = None
        self.hydra_context: Optional[HydraContext] = None
        self.executor = None
        self.mp_config = kwargs

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
        self.condition = mp.Condition()
        self.executor = NestablePool(**self.mp_config)

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        from . import _core

        return _core.launch(
            launcher=self, job_overrides=job_overrides, initial_job_idx=initial_job_idx
        )
    
    def launch_experiment_sequence(
        self, job_overrides: ExperimentSequence, initial_job_idx: int
    ) -> Sequence[JobReturn]:
        from . import _core

        return _core.launch(
            launcher=self, job_overrides=job_overrides, initial_job_idx=initial_job_idx
        )
    
    def __del__(self):
        if self.executor:
            self.executor.close()
            del self.executor