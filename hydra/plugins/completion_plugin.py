# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import ABCMeta
from abc import abstractmethod
from omegaconf import DictConfig, ListConfig
import six

from hydra.plugins import Plugin


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

    @abstractmethod
    def query(self, config_loader, cfg):
        raise NotImplementedError()

    @staticmethod
    def _complete(config_loader, line, index):
        # print("line=|{}|,index={}".format(line.replace(" ", "_"), index))
        line = line.rstrip()
        if index is None:
            index = len(line)
        if len(line) > 0:
            line = line[0:index]
        words = line.split(" ")
        config = config_loader.load_configuration(words[0:-1])
        cur_word = words[-1]

        value = config.select(cur_word) if cur_word != "" else config
        if isinstance(value, DictConfig):
            # dict
            if value is config:
                # top level, do not prepend .
                return sorted(value.keys())
            else:
                return [".{}".format(key) for key in sorted(value.keys())]
        elif isinstance(value, ListConfig):
            # list
            return [".{}".format(i) for i in range(len(value))]
        else:
            # primitive
            return ["{}".format(str(value))]
