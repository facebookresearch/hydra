# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.plugins.completion_plugin import CompletionPlugin


class ZshCompletion(CompletionPlugin):
    def install(self):
        pass

    def uninstall(self):
        pass

    def provides(self):
        return "zsh"

    def query(self):
        pass
