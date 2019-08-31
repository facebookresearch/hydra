# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra.plugins import SearchPathPlugin


class FAIRClusterDefaults(SearchPathPlugin):
    def manipulate_search_path(self, search_path):
        print("FAIRClusterDefaults")
        pass
