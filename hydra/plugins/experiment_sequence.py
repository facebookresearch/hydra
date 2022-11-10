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

from abc import abstractmethod
import typing

from collections.abc import Iterator
from typing import Any, Sequence, Tuple


class ExperimentSequence(Iterator):
    @abstractmethod
    def __next__(self):
        """Return tuple of experiment id, optional trial object and experiment overrides."""
        raise NotImplementedError()
    
    def __iter__(self) -> typing.Iterator[Sequence[str]]:
        return self
    
    @abstractmethod
    def update_sequence(self, experiment_result: Tuple[Sequence[str], Any]):
        """Update experiment generator(study) with experiment results"""
        raise NotImplementedError()
    
    def __len__(self):
        """Return maximum number of experiments sequence can produce"""
        raise NotImplementedError()