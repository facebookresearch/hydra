# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

"""
Basic sweeper can generate cartesian products of multiple input commands, each with a
comma separated list of values.
for example, for:
python foo.py a=1,2,3 b=10,20
Basic Sweeper would generate 6 jobs:
1,10
1,20
2,10
2,20
3,10
3,20
"""
import copy
import itertools
from typing import Optional, Sequence

from hydra.plugins.common.utils import JobReturn
from hydra.plugins.step_sweeper import StepSweeper


class BasicSweeper(StepSweeper):
    """
    Basic sweeper
    """

    def __init__(self) -> None:
        """
        Instantiates
        """
        super(BasicSweeper, self).__init__()
        self.job_results: Optional[Sequence[JobReturn]] = None

    def get_job_batch(self) -> Sequence[Sequence[str]]:
        """
        :return: A list of lists of strings, each inner list is the overrides for a single job
        that should be executed.
        """

        assert self.arguments is not None
        lists = []
        for s in self.arguments:
            key, value = s.split("=")
            lists.append(["{}={}".format(key, val) for val in value.split(",")])

        return list(itertools.product(*lists))

    def is_done(self) -> bool:
        # just one batch
        return self.job_results is not None

    def update_results(self, job_results: Sequence[JobReturn]) -> None:
        self.job_results = copy.copy(job_results)
