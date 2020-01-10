# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

# TODO: move to _internal.config and split into search_path and ConfigSearchPath (maybe renaming in the process)


class SearchPath:
    def __init__(self, provider: Optional[str], search_path: Optional[str]):
        self.provider = provider
        self.path = search_path

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"provider={self.provider}, path={self.path}"


class ConfigSearchPath:
    config_search_path: List[SearchPath]

    def __init__(self) -> None:
        self.config_search_path = []

    def find_last_match(self, reference: SearchPath) -> int:
        return self.find_match(reference, reverse=True)

    def find_first_match(self, reference: SearchPath) -> int:
        return self.find_match(reference, reverse=False)

    def find_match(self, reference: SearchPath, reverse: bool) -> int:
        p = self.config_search_path
        if reverse:
            iterator = zip(reversed(range(len(p))), reversed(p))
        else:
            iterator = zip(range(len(p)), p)
        for idx, sp in iterator:
            has_prov = reference.provider is not None
            has_path = reference.path is not None
            if has_prov and has_path:
                if reference.provider == sp.provider and reference.path == sp.path:
                    return idx
            elif has_prov:
                if reference.provider == sp.provider:
                    return idx
            elif has_path:
                if reference.path == sp.path:
                    return idx
            else:
                assert False
        return -1

    def append(
        self, provider: str, path: str, anchor: Optional[SearchPath] = None
    ) -> None:
        """
        :param provider: who is providing this search path, can be Hydra,
               the @hydra.main() function, or individual plugins or libraries.
        :param path: path element, can be a file system path or a package path (For example pkg://hydra.conf)
        :param anchor: if string, acts as provider. if SearchPath can be used to match against provider and / or path
        :return:
        """
        if anchor is None:
            self.config_search_path.append(SearchPath(provider, path))
        else:
            if isinstance(anchor, str):
                anchor = SearchPath(anchor, None)

            idx = self.find_last_match(anchor)
            if idx != -1:
                self.config_search_path.insert(idx + 1, SearchPath(provider, path))
            else:
                self.append(provider, path, anchor=None)

    def prepend(
        self, provider: str, path: str, anchor: Optional[SearchPath] = None
    ) -> None:
        if anchor is None:
            self.config_search_path.insert(0, SearchPath(provider, path))
        else:
            if isinstance(anchor, str):
                anchor = SearchPath(anchor, None)

            idx = self.find_first_match(anchor)
            if idx != -1:
                if idx > 0:
                    self.config_search_path.insert(idx, SearchPath(provider, path))
                else:
                    self.prepend(provider, path, None)
            else:
                self.prepend(provider, path, None)

    def __str__(self) -> str:
        return str(self.config_search_path)
