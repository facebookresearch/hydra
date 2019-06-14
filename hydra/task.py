class Task:
    """
    A high level task, for example Object classification or Language modeling.
    Anything that has configuration needs ranging from trivial to extremely complex
    """

    def setup(self, cfg):
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
