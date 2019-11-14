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

from hydra.plugins.step_sweeper import StepSweeper


class BasicSweeper(StepSweeper):
    """
    Basic sweeper
    """

    def __init__(self):
        """
        Instantiates
        """
        super(BasicSweeper, self).__init__()
        self.job_results = None

    def get_job_batch(self):
        """
        :return: A list of lists of strings, each inner list is the overrides for a single job
        that should be executed.
        """

        lists = []
        for s in self.arguments:
            key, value = s.split("=")
            lists.append(["{}={}".format(key, val) for val in value.split(",")])

        return list(itertools.product(*lists))

    def is_done(self):
        # just one batch
        return self.job_results is not None

    def update_results(self, job_results):
        self.job_results = copy.copy(job_results)
