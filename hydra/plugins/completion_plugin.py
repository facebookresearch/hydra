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
        if isinstance(config, Config):
            if word.endswith(".") or word.endswith("="):
                exact_key = word[0:-1]
                conf_node = config.select(exact_key)
                if conf_node is not None:
                    if isinstance(conf_node, Config):
                        key_matches = CompletionPlugin._get_matches(conf_node, "")
                    else:
                        # primitive
                        key_matches = [conf_node]
                else:
                    key_matches = []

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
                    if isinstance(config, DictConfig):
                        for key, value in config.items():
                            if key.startswith(word):
                                matches.append(str_rep(key, value))
                    elif isinstance(config, ListConfig):
                        for idx, value in enumerate(config):
                            if str(idx).startswith(word):
                                matches.append(str_rep(idx, value))
        else:
            assert False, "Object is not an instance of config : {}".format(
                type(config)
            )

        return matches

    def _query_config_groups(self, word):
        last_eq_index = word.rfind("=")
        last_slash_index = word.rfind("/")
        if last_eq_index != -1:
            parent_group = word[0:last_eq_index]
            file_type = "file"
        else:
            file_type = "dir"
            if last_slash_index == -1:
                parent_group = ""
            else:
                parent_group = word[0:last_slash_index]

        all_matched_groups = self.config_loader.get_group_options(
            parent_group, file_type=file_type
        )
        matched_groups = []
        if file_type == "file":
            for match in all_matched_groups:
                name = (
                    "{}={}".format(parent_group, match) if parent_group != "" else match
                )
                if name.startswith(word):
                    matched_groups.append(name)
        elif file_type == "dir":
            for match in all_matched_groups:
                name = (
                    "{}/{}".format(parent_group, match) if parent_group != "" else match
                )
                if name.startswith(word):
                    files = self.config_loader.get_group_options(name, file_type="file")
                    dirs = self.config_loader.get_group_options(name, file_type="dir")
                    if len(dirs) == 0 and len(files) > 0:
                        name = name + "="
                    elif len(dirs) > 0 and len(files) == 0:
                        name = name + "/"
                    matched_groups.append(name)

        return matched_groups

    def _query(self, line):
        args = line.split(" ")
        words = []
        word = args[-1]
        if len(args) > 1:
            words = args[0:-1]

        config = self.config_loader.load_configuration(words)
        config_matches = CompletionPlugin._get_matches(config, word)
        matched_groups = self._query_config_groups(word)

        return sorted(list(set(matched_groups + config_matches)))
