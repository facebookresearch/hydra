# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import ABCMeta
from abc import abstractmethod
from omegaconf import DictConfig, ListConfig, Config
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
    def _get_matches(config, word):
        def str_rep(in_key, in_value):
            if isinstance(in_value, Config):
                return "{}.".format(in_key)
            else:
                return "{}=".format(in_key)

        matches = []
        if isinstance(config, DictConfig):
            if word.endswith(".") or word.endswith("="):
                exact_key = word[0:-1]
                conf_node = config.select(exact_key)

                if isinstance(conf_node, Config):
                    key_matches = CompletionPlugin._get_matches(conf_node, "")
                else:
                    # primitive
                    key_matches = [conf_node]

                matches.extend(["{}{}".format(word, match) for match in key_matches])
            else:
                last_dot = word.rfind(".")
                if last_dot != -1:
                    base_key = word[0:last_dot]
                    partial_key = word[last_dot + 1 :]
                    conf_node = config.select(base_key)
                    key_matches = CompletionPlugin._get_matches(conf_node, partial_key)
                    matches.extend(
                        ["{}.{}".format(base_key, match) for match in key_matches]
                    )
                else:
                    for key, value in config.items():
                        if key.startswith(word):
                            matches.append(str_rep(key, value))
        elif isinstance(config, ListConfig):
            # TODO
            matches = []
        else:
            assert False

        return sorted(matches)

    @staticmethod
    def _complete(config_loader, line, index):
        line = line.rstrip()
        if index is None:
            index = len(line)
        if len(line) > 0:
            line = line[0:index]
        words = line.split(" ")
        config = config_loader.load_configuration(words[0:-1])

        return CompletionPlugin._get_matches(config, words[-1])
