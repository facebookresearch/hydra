import copy

from . import utils
from .sweeper import Sweeper


class BasicSweeper(Sweeper):

    def __init__(self):
        self.arguments = None
        self.job_results = None

    def setup(self, hydra_cfg, arguments):
        """
        :param hydra_cfg: hydra configuration object
        :param arguments: +
        :return: 
        """
        self.arguments = arguments

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
