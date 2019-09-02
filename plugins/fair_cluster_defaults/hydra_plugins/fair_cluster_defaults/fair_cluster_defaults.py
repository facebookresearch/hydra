# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra.plugins import SearchPathPlugin
from hydra._internal.config_search_path import ConfigSearchPath


class FAIRClusterDefaults(SearchPathPlugin):
    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        search_path.prepend(
            "fair-cluster-defaults",
            "pkg://hydra_plugins.fair_cluster_defaults.conf",
            anchor="hydra",
        )
