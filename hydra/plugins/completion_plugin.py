# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

# TODO: Test with /miniconda3/envs/hydra36/bin/python , seems to be running python for some reason.
# TODO: Add tests for completion with +prefix (should suggest config groups that are not listed)
# TODO: Test completion when defaults has a missing mandatory item


import os
import re
import sys
from abc import abstractmethod
from omegaconf import (
    Container,
    DictConfig,
    MissingMandatoryValue,
    OmegaConf,
    ListConfig,
)
from typing import Any, List, Optional, Tuple, Union

from hydra.core.config_loader import ConfigLoader
from hydra.core.object_type import ObjectType
from hydra.plugins.plugin import Plugin
from hydra.types import RunMode


class CompletionPlugin(Plugin):
    def __init__(self, config_loader: ConfigLoader) -> None:
        self.config_loader = config_loader

    @abstractmethod
    def install(self) -> None:
        ...

    @abstractmethod
    def uninstall(self) -> None:
        ...

    @staticmethod
    @abstractmethod
    def provides() -> str:
        """
        :return: the name of the shell this plugin provides completion for
        """
        ...

    @abstractmethod
    def query(self, config_name: Optional[str]) -> None:
        ...

    @staticmethod
    @abstractmethod
    def help(command: str) -> str:
        """
        :param command: "install" or "uninstall"
        :return: command the user can run to install or uninstall this shell completion on the appropriate shell
        """
        ...

    @staticmethod
    def _get_filename(filename: str) -> Tuple[Optional[str], Optional[str]]:
        last = filename.rfind("=")
        if last != -1:
            key_eq = filename[0 : last + 1]
            filename = filename[last + 1 :]
            prefixes = [".", "/", "\\", "./", ".\\"]
            if sys.platform.startswith("win"):
                for drive in range(ord("a"), ord("z")):
                    prefixes.append(f"{chr(drive)}:")

            if not filename:
                return None, None
            for prefix in prefixes:
                if filename.lower().startswith(prefix):
                    return key_eq, filename
        return None, None

    @staticmethod
    def complete_files(word: str) -> List[str]:
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
    def _get_matches(config: Container, word: str) -> List[str]:
        def str_rep(in_key: Union[str, int], in_value: Any) -> str:
            if OmegaConf.is_config(in_value):
                return f"{in_key}."
            else:
                return f"{in_key}="

        if config is None:
            return []
        elif OmegaConf.is_config(config):
            matches = []
            if word.endswith(".") or word.endswith("="):
                exact_key = word[0:-1]
                try:
                    conf_node = OmegaConf.select(
                        config, exact_key, throw_on_missing=True
                    )
                except MissingMandatoryValue:
                    conf_node = ""
                if conf_node is not None:
                    if OmegaConf.is_config(conf_node):
                        key_matches = CompletionPlugin._get_matches(conf_node, "")
                    else:
                        # primitive
                        if isinstance(conf_node, bool):
                            conf_node = str(conf_node).lower()
                        key_matches = [conf_node]
                else:
                    key_matches = []

                matches.extend([f"{word}{match}" for match in key_matches])
            else:
                last_dot = word.rfind(".")
                if last_dot != -1:
                    base_key = word[0:last_dot]
                    partial_key = word[last_dot + 1 :]
                    conf_node = OmegaConf.select(config, base_key)
                    key_matches = CompletionPlugin._get_matches(conf_node, partial_key)
                    matches.extend([f"{base_key}.{match}" for match in key_matches])
                else:
                    if isinstance(config, DictConfig):
                        for key, value in config.items_ex(resolve=False):
                            if key.startswith(word):
                                matches.append(str_rep(key, value))
                    elif OmegaConf.is_list(config):
                        assert isinstance(config, ListConfig)
                        for idx in range(len(config)):
                            try:
                                value = config[idx]
                                if str(idx).startswith(word):
                                    matches.append(str_rep(idx, value))
                            except MissingMandatoryValue:
                                matches.append(str_rep(idx, ""))

        else:
            assert False, f"Object is not an instance of config : {type(config)}"

        return matches

    def _query_config_groups(self, word: str) -> Tuple[List[str], bool]:
        last_eq_index = word.rfind("=")
        last_slash_index = word.rfind("/")
        exact_match: bool = False
        if last_eq_index != -1:
            parent_group = word[0:last_eq_index]
            results_filter = ObjectType.CONFIG
        else:
            results_filter = ObjectType.GROUP
            if last_slash_index == -1:
                parent_group = ""
            else:
                parent_group = word[0:last_slash_index]

        all_matched_groups = self.config_loader.get_group_options(
            group_name=parent_group, results_filter=results_filter
        )
        matched_groups: List[str] = []
        if results_filter == ObjectType.CONFIG:
            for match in all_matched_groups:
                name = f"{parent_group}={match}" if parent_group != "" else match
                if name.startswith(word):
                    matched_groups.append(name)
                exact_match = True
        elif results_filter == ObjectType.GROUP:
            for match in all_matched_groups:
                name = f"{parent_group}/{match}" if parent_group != "" else match
                if name.startswith(word):
                    files = self.config_loader.get_group_options(
                        group_name=name, results_filter=ObjectType.CONFIG
                    )
                    dirs = self.config_loader.get_group_options(
                        group_name=name, results_filter=ObjectType.GROUP
                    )
                    if len(dirs) == 0 and len(files) > 0:
                        name = name + "="
                    elif len(dirs) > 0 and len(files) == 0:
                        name = name + "/"
                    matched_groups.append(name)

        return matched_groups, exact_match

    def _query(self, config_name: Optional[str], line: str) -> List[str]:
        from .._internal.utils import get_args

        new_word = len(line) == 0 or line[-1] == " "
        parsed_args = get_args(line.split())
        words = parsed_args.overrides
        if new_word or len(words) == 0:
            word = ""
        else:
            word = words[-1]
            words = words[0:-1]

        run_mode = RunMode.MULTIRUN if parsed_args.multirun else RunMode.RUN
        config = self.config_loader.load_configuration(
            config_name=config_name, overrides=words, run_mode=run_mode, strict=True
        )

        fname_prefix, filename = CompletionPlugin._get_filename(word)
        if filename is not None:
            assert fname_prefix is not None
            result = CompletionPlugin.complete_files(filename)
            result = [fname_prefix + file for file in result]
        else:
            matched_groups, exact_match = self._query_config_groups(word)
            config_matches: List[str] = []
            if not exact_match:
                config_matches = CompletionPlugin._get_matches(config, word)
            result = list(set(matched_groups + config_matches))

        return sorted(result)

    @staticmethod
    def strip_python_or_app_name(line: str) -> str:
        """
        Take the command line received from shell completion, and strip the app name from it
        which could be at the form of python script.py or some_app.
        it also corrects the key (COMP_INDEX) to reflect the same location in the striped command line.
        :param line: input line, may contain python file.py followed=by_args..
        :return: tuple(args line, key of cursor in args line)
        """
        python_args = r"^\s*[\w\/]*python[3]?\s*[\w/\.]*\s*(.*)"
        app_args = r"^\s*[\w_\-=\./]+\s*(.*)"
        match = re.match(python_args, line)
        if match:
            return match.group(1)
        else:
            match = re.match(app_args, line)
            if match:
                return match.group(1)
            else:
                raise RuntimeError(f"Error parsing line '{line}'")


class DefaultCompletionPlugin(CompletionPlugin):
    """
    A concrete instance of CompletionPlugin that is used for testing.
    """

    def install(self) -> None:
        ...

    def uninstall(self) -> None:
        ...

    @staticmethod
    def provides() -> str:
        ...

    def query(self, config_name: Optional[str]) -> None:
        ...

    @staticmethod
    def help(command: str) -> str:
        ...
