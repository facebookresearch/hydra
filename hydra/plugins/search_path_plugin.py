from .plugin import Plugin
from abc import abstractmethod


class SearchPathPlugin(Plugin):
    @abstractmethod
    def manipulate_search_path(self, search_path):
        """
        Allows the plugin to manipulate the search path
        """
        raise NotImplementedError()
