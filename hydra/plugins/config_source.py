# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings

import re

from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict

from omegaconf import Container, OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.plugin import Plugin


@dataclass
class ConfigResult:
    provider: str
    path: str
    config: Container
    header: Dict[str, str]
    is_schema_source: bool = False


class ConfigLoadError(IOError):
    pass


class ConfigSource(Plugin):
    provider: str
    path: str

    def __init__(self, provider: str, path: str) -> None:
        if not path.startswith(self.scheme()):
            raise ValueError("Invalid path")
        self.provider = provider
        self.path = path[len(self.scheme() + "://") :]

    @staticmethod
    @abstractmethod
    def scheme() -> str:
        """
        :return: the scheme for this config source, for example file:// or pkg://
        """
        ...

    @abstractmethod
    def load_config(self, config_path: str) -> ConfigResult:
        ...

    # subclasses may override to improve performance
    def exists(self, config_path: str) -> bool:
        return self.is_group(config_path) or self.is_config(config_path)

    @abstractmethod
    def is_group(self, config_path: str) -> bool:
        ...

    @abstractmethod
    def is_config(self, config_path: str) -> bool:
        ...

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        """
        List items under the specified config path
        :param config_path: config path to list items in, examples: "", "foo", "foo/bar"
        :param results_filter: None for all, GROUP for groups only and CONFIG for configs only
        :return: a list of config or group identifiers (sorted and unique)
        """
        ...

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"provider={self.provider}, path={self.scheme()}://{self.path}"

    def _list_add_result(
        self,
        files: List[str],
        file_path: str,
        file_name: str,
        results_filter: Optional[ObjectType],
    ) -> None:
        filtered = ["__pycache__", "__init__.py"]
        is_group = self.is_group(file_path)
        is_config = self.is_config(file_path)
        if (
            is_group
            and (results_filter is None or results_filter == ObjectType.GROUP)
            and file_name not in filtered
        ):
            files.append(file_name)
        if (
            is_config
            and file_name not in filtered
            and (results_filter is None or results_filter == ObjectType.CONFIG)
        ):
            # strip extension
            last_dot = file_name.rfind(".")
            if last_dot != -1:
                file_name = file_name[0:last_dot]

            files.append(file_name)

    def full_path(self) -> str:
        return f"{self.scheme()}://{self.path}"

    @staticmethod
    def _normalize_file_name(filename: str) -> str:
        if not any(filename.endswith(ext) for ext in [".yaml", ".yml"]):
            filename += ".yaml"
        return filename

    @staticmethod
    def _update_package_in_header(
        header: Dict[str, str], normalized_config_path: str
    ) -> None:
        config_without_ext = normalized_config_path[0 : -len(".yaml")]
        last = config_without_ext.rfind("/")
        if last == -1:
            group = ""
            name = config_without_ext
        else:
            group = config_without_ext[0:last]
            name = config_without_ext[last + 1 :]

        if "package" not in header:
            header["package"] = "_global_"
            # TODO: warn the user if we are defaulting
            # to _global_ and they should make an explicit selection recommended  _group_.
            msg = f"""Warning: Missing # @package directive in {normalized_config_path}.
Recommendation: add “# @package _group_” at the top of {normalized_config_path} and
remove the package ‘{group.replace("/", ".")}:’ from your file, de-indenting its children.
More information at <link>.
"""
            msg = f"{normalized_config_path}"
            warnings.warn(message=msg, category=UserWarning)

        package = header["package"]

        if package == "_global_":
            # default to the global behavior to remain backward compatible.
            package = ""
        else:
            package = package.replace("_group_", group).replace("/", ".")
            package = package.replace("_name_", name)

        header["package"] = package

    @staticmethod
    def _embed_config(node: Container, package: str) -> Container:
        if package == "_global_":
            package = ""

        if package is not None and package != "":
            cfg = OmegaConf.create()
            OmegaConf.update(cfg, package, OmegaConf.structured(node))
        else:
            cfg = OmegaConf.structured(node)
        return cfg

    @staticmethod
    def _get_header_dict(config_text: str) -> Dict[str, str]:
        res = {}
        for line in config_text.splitlines():
            line = line.strip()
            if len(line) == 0:
                # skip empty lines in header
                continue
            if re.match("^\\s*#\\s*@", line):
                line = line.lstrip("#").strip()
                splits = re.split(" |:", line)
                splits = list(filter(lambda x: len(x) > 0, splits))
                if len(splits) < 2:
                    raise ValueError(f"Expected header format: KEY VALUE, got '{line}'")
                if len(splits) > 2:
                    raise ValueError(f"Too many components in '{line}'")
                key, val = splits[0], splits[1]
                key = key.strip()
                val = val.strip()
                if key.startswith("@"):
                    res[key[1:]] = val
            else:
                # stop parsing header on first non-header line
                break

        return res
