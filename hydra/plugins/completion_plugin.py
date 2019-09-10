# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from abc import ABCMeta
from omegaconf import DictConfig, ListConfig, Config
import six

from hydra.plugins import Plugin


@six.add_metaclass(ABCMeta)
class CompletionPlugin(Plugin):
    def __init__(self, config_loader):
        self.config_loader = config_loader

    def install(self):
        raise NotImplementedError()

    def uninstall(self):
        raise NotImplementedError()

    def provides(self):
        """
        :return: the name of the shell this plugin provides completion for
        """
        return None

    def query(self):
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

    def _post_process_suggestions(self, suggestions, word):
        return suggestions

    def _query(self, line, index):
        # if index is None:
        #     index = len(line)

        args = line.split(" ")
        words = []
        word = args[-1]
        if len(args) > 1:
            words = args[0:-1]

        config = self.config_loader.load_configuration(words)
        suggestions = CompletionPlugin._get_matches(config, word)
        return self._post_process_suggestions(suggestions, word)
