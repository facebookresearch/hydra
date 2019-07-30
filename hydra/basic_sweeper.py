import copy

from . import utils
from .sweeper import StepSweeper


class BasicSweeper(StepSweeper):

    def __init__(self):
        self.job_results = None

    def get_job_batch(self):
        """
        :return: A list of lists of strings, each inner list is the overrides for a single job
        that should be executed.
        """
        return utils.get_sweep(self.arguments)

    def is_done(self):
        # just one batch
        return self.job_results is not None

    def update_results(self, job_results):
        self.job_results = copy.copy(job_results)
