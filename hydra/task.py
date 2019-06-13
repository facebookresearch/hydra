class Task:
    """
    A task represents a high level task, that can be broken down into subtasks.
    Examples:
        for a task of model based reinforcement learning, subtasks can be cartpole and halfcheetah
        For a task of image classification, subtasks can be imagenet and cifar10.

        The task code is expected to be able to deal with all the subtasks. the configuration passed will configure
        the behavior of the task.
    """

    def setup(self, log, cfg):
        """
        Setup your Task object, initialize various members etc
        :param cfg OmegaConf configuration object
        """
        raise NotImplemented()

    def run(self, cfg):
        """
        Solve your problem, this is typically a training loop or something similar
        :param cfg OmegaConf configuration object
        """
        raise NotImplemented()

    # TODO: checkpoint handling?