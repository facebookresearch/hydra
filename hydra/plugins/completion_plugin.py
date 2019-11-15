# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys
from abc import ABCMeta
from abc import abstractmethod
import six
from omegaconf import DictConfig, ListConfig, Config, MissingMandatoryValue

from hydra.plugins import Plugin


@six.add_metaclass(ABCMeta)
class CompletionPlugin(Plugin):
    def __init__(self, config_loader):
        self.config_loader = config_loader

    def install(self):
        raise NotImplementedError()

    def uninstall(self):
        raise NotImplementedError()

    @abstractmethod
    def provides(self):
        """
        :return: the name of the shell this plugin provides completion for
        """
        return None

    def query(self, config_file):
        raise NotImplementedError()

    @staticmethod
    def _get_filename(fname):
        last = fname.rfind("=")
        if last != -1:
            key_eq = fname[0 : last + 1]
            fname = fname[last + 1 :]
            prefixes = [".", "/", "\\", "./", ".\\"]
            if sys.platform.startswith("win"):
                for drive in range(ord("a"), ord("z")):
                    prefixes.append("{}:".format(chr(drive)))

            if not fname:
                return None, None
            lowerfilename = fname.lower()
            for prefix in prefixes:
                if lowerfilename.startswith(prefix):
                    return key_eq, fname
        return None, None

    @staticmethod
    def complete_files(word):
        if os.path.isdir(word):
            dirname = word
            files = os.listdir(word)
            file_prefix = ""
        else:
            dirname = os.path.dirname(word)
            if os.path.isdir(dirname):
                files = os.listdir(dirname)
            else:
                files = []
            file_prefix = os.path.basename(word)
        ret = []
        for file in files:
            if file.startswith(file_prefix):
                ret.append(os.path.join(dirname, file))
        return ret

    @staticmethod
    def _get_matches(config, word):
        def str_rep(in_key, in_value):
            if isinstance(in_value, Config):
                return "{}.".format(in_key)
            else:
                return "{}=".format(in_key)

        if config is None:
            return []
        elif isinstance(config, Config):
            matches = []
            if word.endswith(".") or word.endswith("="):
                exact_key = word[0:-1]
                try:
                    conf_node = config.select(exact_key)
                except MissingMandatoryValue:
                    conf_node = ""
                if conf_node is not None:
                    if isinstance(conf_node, Config):
                        key_matches = CompletionPlugin._get_matches(conf_node, "")
                    else:
                        # primitive
                        if isinstance(conf_node, bool):
                            conf_node = str(conf_node).lower()
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
                        for key, value in config.items(resolve=False):
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
        exact_match = False
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
                exact_match = True
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

        return matched_groups, exact_match

    def _query(self, config_file, line):
        from .._internal.utils import get_args

        new_word = len(line) == 0 or line[-1] == " "
        parsed_args = get_args(line.split())
        words = parsed_args.overrides
        if new_word or len(words) == 0:
            word = ""
        else:
            word = words[-1]
            words = words[0:-1]

        config = self.config_loader.load_configuration(
            config_file=config_file, overrides=words, strict=True
        )

        fname_prefix, filename = CompletionPlugin._get_filename(word)
        if filename is not None:
            result = CompletionPlugin.complete_files(filename)
            result = [fname_prefix + file for file in result]
        else:
            matched_groups, exact_match = self._query_config_groups(word)
            config_matches = []
            if not exact_match:
                config_matches = CompletionPlugin._get_matches(config, word)
            result = list(set(matched_groups + config_matches))

        return sorted(result)


@six.add_metaclass(ABCMeta)
class DefaultCompletionPlugin(CompletionPlugin):
    """
    A concrete instance of CompletionPlugin that is used for testing.
    """

    def provides(self):
        return None
