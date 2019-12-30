# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import abstractmethod

from .plugin import Plugin


class SearchPathPlugin(Plugin):
    @abstractmethod
    def manipulate_search_path(self, search_path):
        """
        Allows the plugin to manipulate the search path
        """
        raise NotImplementedError()
