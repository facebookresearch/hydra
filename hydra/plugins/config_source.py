# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy

from textwrap import dedent

import warnings

import re

from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple, MutableSequence

from hydra.core import DefaultElement
from hydra.core.NewDefaultElement import InputDefault
from hydra.errors import HydraException
from omegaconf import (
    Container,
    OmegaConf,
    ListConfig,
    DictConfig,
    open_dict,
    read_write,
)

from hydra.core.object_type import ObjectType
from hydra.plugins.plugin import Plugin


@dataclass
class ConfigResult:
    provider: str
    path: str
    config: Container
    header: Dict[str, str]
    defaults_list: List[DefaultElement]
    new_defaults_list: List[InputDefault]
    is_schema_source: bool = False


class ConfigLoadError(HydraException, IOError):
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
    def load_config(
        self,
        config_path: str,
        is_primary_config: bool,
        package_override: Optional[str] = None,
    ) -> ConfigResult:
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

    @abstractmethod
    def available(self) -> bool:
        """
        :return: True is this config source is pointing to a valid location
        """
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
    def _resolve_package(
        config_without_ext: str, header: Dict[str, str], package_override: Optional[str]
    ) -> str:
        last = config_without_ext.rfind("/")
        if last == -1:
            group = ""
            name = config_without_ext
        else:
            group = config_without_ext[0:last]
            name = config_without_ext[last + 1 :]

        if "package" in header:
            package = header["package"]
        else:
            package = ""

        if package_override is not None:
            package = package_override

        if package == "_global_":
            package = ""
        else:
            package = package.replace("_group_", group).replace("/", ".")
            package = package.replace("_name_", name)

        return package

    def _update_package_in_header(
        self,
        header: Dict[str, str],
        normalized_config_path: str,
        is_primary_config: bool,
        package_override: Optional[str],
    ) -> None:
        config_without_ext = normalized_config_path[0 : -len(".yaml")]

        if "package" in header:
            # keep a backup of the original package header
            # TODO: clean up manipulation of pacakge header in config sources
            header["orig_package"] = header["package"]

        package = ConfigSource._resolve_package(
            config_without_ext=config_without_ext,
            header=header,
            package_override=package_override,
        )

        # TODO: cleanup
        # if is_primary_config:
        #     if "package" not in header:
        #         header["package"] = "_global_"
        #     else:
        #         if package != "":
        #             raise HydraException(
        #                 f"Primary config '{config_without_ext}' must be "
        #                 f"in the _global_ package; effective package : '{package}'"
        #             )
        # else:
        #     if "package" not in header:
        #         # Loading a config group option.
        #         # Hydra 1.0: default to _global_ and warn.
        #         # Hydra 1.1: default will change to _package_ and the warning will be removed.
        #         header["package"] = "_global_"
        #         msg = (
        #             f"\nMissing @package directive {normalized_config_path} in {self.full_path()}.\n"
        #             f"See https://hydra.cc/docs/next/upgrades/0.11_to_1.0/adding_a_package_directive"
        #         )
        #         warnings.warn(message=msg, category=UserWarning)

        header["package"] = package

    @staticmethod
    def _embed_config(node: Container, package: str) -> Container:
        if package == "_global_":
            package = ""

        if package is not None and package != "":
            cfg = OmegaConf.create()
            OmegaConf.update(cfg, package, node, merge=False)
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
                splits = re.split(" ", line)
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

    @staticmethod
    def _split_group(
        group_with_package: str,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        idx = group_with_package.find("@")
        if idx == -1:
            # group
            group = group_with_package
            package = None
        else:
            # group@package
            group = group_with_package[0:idx]
            package = group_with_package[idx + 1 :]

        package2 = None
        if package is not None:
            # if we have a package, break it down if it's a rename
            idx = package.find(":")
            if idx != -1:
                package2 = package[idx + 1 :]
                package = package[0:idx]

        if package == "":
            package = None

        if package2 == "":
            package2 = None

        return group, package, package2

    @staticmethod
    def _create_defaults_list(
        config_path: Optional[str],
        defaults: ListConfig,
    ) -> List[DefaultElement]:
        if not isinstance(defaults, MutableSequence):
            raise ValueError(
                dedent(
                    f"""\
                    Invalid defaults list in '{config_path}', defaults must be a list.
                    Example of a valid defaults:
                    defaults:
                      - dataset: imagenet
                      - model: alexnet
                        optional: true
                      - optimizer: nesterov
                    """
                )
            )
        defaults = copy.deepcopy(defaults)
        res: List[DefaultElement] = []
        for item in defaults:
            if isinstance(item, DictConfig):
                optional = False
                if "optional" in item:
                    optional = item.pop("optional")
                keys = list(item.keys())
                if len(keys) > 1:
                    raise ValueError(f"Too many keys in default item {item}")
                if len(keys) == 0:
                    raise ValueError(f"Missing group name in {item}")
                key = keys[0]
                config_group, package, package2 = ConfigSource._split_group(key)
                node = item._get_node(key)
                assert node is not None
                config_name = node._value()

                is_delete = False
                if config_name is None:
                    warnings.warn(
                        category=UserWarning,
                        message=dedent(
                            f"""
                    Deprecated form of deletion used in the defaults list of '{config_path}'.
                    'group: null' is deprecated, use '~group' instead.
                    You can also delete group with a specific value with '~group: value'.
                    Support for the 'group: null' form will be removed in Hydra 1.2.
                    """
                        ),
                    )
                    is_delete = True
                elif config_group.startswith("~"):
                    is_delete = True
                    config_group = config_group[1:]

                default = DefaultElement(
                    config_group=config_group,
                    config_name=config_name,
                    package=package,
                    rename_package_to=package2,
                    optional=optional,
                    is_delete=is_delete,
                    parent=config_path,
                )
            elif isinstance(item, str):
                if item.startswith("~"):
                    item = item[1:]
                    default = DefaultElement(
                        config_group=item,
                        config_name="_delete_",
                        is_delete=True,
                        parent=config_path,
                    )
                else:
                    default = DefaultElement(
                        config_group=None,
                        config_name=item,
                        parent=config_path,
                    )
            else:
                raise ValueError(
                    f"Unsupported type in defaults : {type(item).__name__}"
                )
            res.append(default)
        return res

    @staticmethod
    def _extract_defaults_list(
        config_path: Optional[str], cfg: Container
    ) -> List[DefaultElement]:
        if not OmegaConf.is_dict(cfg):
            return []

        assert isinstance(cfg, DictConfig)
        with read_write(cfg):
            with open_dict(cfg):
                defaults = cfg.pop("defaults", OmegaConf.create([]))

        if len(defaults) > 0:
            return ConfigSource._create_defaults_list(
                config_path=config_path, defaults=defaults
            )
        else:
            return []

    @staticmethod
    def _create_new_defaults_list(
        defaults: ListConfig,
    ) -> List[InputDefault]:
        res: List[DefaultElement] = []
        for item in defaults:
            if isinstance(item, DictConfig):
                optional = False
                if "optional" in item:
                    optional = item.pop("optional")
                keys = list(item.keys())
                if len(keys) > 1:
                    raise ValueError(f"Too many keys in default item {item}")
                if len(keys) == 0:
                    raise ValueError(f"Missing group name in {item}")
                key = keys[0]
                config_group, package, _package2 = ConfigSource._split_group(key)
                node = item._get_node(key)
                assert node is not None
                config_name = node._value()

                default = InputDefault(
                    group=config_group,
                    name=config_name,
                    package=package,
                    optional=optional,
                )
            elif isinstance(item, str):
                path, package, _package2 = ConfigSource._split_group(item)
                default = InputDefault(name=path, package=package)
            else:
                raise ValueError(
                    f"Unsupported type in defaults : {type(item).__name__}"
                )
            res.append(default)
        return res

    @staticmethod
    def _extract_raw_defaults_list(cfg: Container) -> List[InputDefault]:
        if not OmegaConf.is_dict(cfg):
            return []

        with read_write(cfg):
            with open_dict(cfg):
                defaults = cfg.pop("defaults", [])

        return defaults
