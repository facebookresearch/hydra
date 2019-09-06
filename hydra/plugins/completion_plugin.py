# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import ABCMeta
from abc import abstractmethod
from hydra.plugins import Plugin

import six


@six.add_metaclass(ABCMeta)
class CompletionPlugin(Plugin):
    @abstractmethod
    def install(self):
        raise NotImplementedError()

    @abstractmethod
    def uninstall(self):
        raise NotImplementedError()

    @abstractmethod
    def provides(self):
        """
        :return: the name of the shell this plugin provides completion for
        """
        raise NotImplementedError()
