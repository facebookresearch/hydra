from abc import abstractmethod


class Sweeper:

    @abstractmethod
    def setup(self, hydra_cfg, arguments):
        """
        :param hydra_cfg: Hydra configuration object
        :param arguments: list of strings describing what this sweeper should do. 
        exact structure is determine by the concrete Sweeper class.
        """
        raise NotImplemented()

    @abstractmethod
    def get_job_batch(self):
        """
        :return: A list of lists of strings, each inner list is the overrides for a single job
        that should be executed.
        """
        raise NotImplemented()

    @abstractmethod
    def is_done(self):
        """
        :return: True if no more batch of jobs should be executed 
        """
        raise NotImplemented()

    @abstractmethod
    def update_results(self, job_results):
        """
        Update the sweeper with the outputs from the last batch of jobs.
        This is useful for sweepers that determine the next batch of jobs based on the results of the last batch
        :param job_results: the outputs from the last batch of jobs.
        """
        raise NotImplemented()
