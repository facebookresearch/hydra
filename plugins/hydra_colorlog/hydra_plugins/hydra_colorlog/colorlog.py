# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra.plugins import SearchPathPlugin
from hydra._internal.config_search_path import ConfigSearchPath


class HydraColorlogSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        # Appends the search path for this plugin to the end of the search path
        search_path.append("hydra-colorlog", "pkg://hydra_plugins.hydra_colorlog.conf")
