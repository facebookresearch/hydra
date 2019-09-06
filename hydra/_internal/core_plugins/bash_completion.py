# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.plugins.completion_plugin import CompletionPlugin
import logging
import sys

log = logging.getLogger(__name__)


class BashCompletion(CompletionPlugin):
    def install(self):
        log.info("Installing bash completion for {}".format(sys.argv[0]))

    def uninstall(self):
        log.info("Uninstalling bash completion for {}".format(sys.argv[0]))

    def provides(self):
        return "bash"
