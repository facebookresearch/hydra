# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.config_search_path import ConfigSearchPath
from hydra.plugins.search_path_plugin import SearchPathPlugin


class HydraColorlogSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append("hydra-colorlog", "pkg://hydra_plugins.hydra_colorlog.conf")
