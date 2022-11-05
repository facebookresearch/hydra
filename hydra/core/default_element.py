# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from dataclasses import dataclass, field
from textwrap import dedent
from typing import List, Optional, Pattern, Union

from omegaconf import AnyNode, DictConfig, OmegaConf
from omegaconf.errors import InterpolationResolutionError

from hydra import version
from hydra._internal.deprecation_warning import deprecation_warning
from hydra.errors import ConfigCompositionException


@dataclass
class ResultDefault:
    config_path: Optional[str] = None
    parent: Optional[str] = None
    package: Optional[str] = None
    is_self: bool = False
    primary: bool = field(default=False, compare=False)

    override_key: Optional[str] = field(default=None, compare=False)

    def __repr__(self) -> str:
        attrs = []
        attr_names = "config_path", "package", "parent"
        for attr in attr_names:
            value = getattr(self, attr)
            if value is not None:
                attrs.append(f'{attr}="{value}"')

        flags = []
        flag_names = ["is_self", "primary"]
        for flag in flag_names:
            value = getattr(self, flag)
            if value:
                flags.append(f"{flag}=True")

        ret = f"{','.join(attrs + flags)}"
        return f"{type(self).__name__}({ret})"


@dataclass
class InputDefault:
    package: Optional[str] = None
    parent_base_dir: Optional[str] = field(default=None, compare=False, repr=False)
    parent_package: Optional[str] = field(default=None, compare=False, repr=False)
    package_header: Optional[str] = field(default=None, compare=False)
    primary: bool = field(default=False, compare=False)

    def is_self(self) -> bool:
        raise NotImplementedError()

    def update_parent(
        self, parent_base_dir: Optional[str], parent_package: Optional[str]
    ) -> None:
        assert self.parent_package is None or self.parent_package == parent_package
        assert self.parent_base_dir is None or self.parent_base_dir == parent_base_dir
        self.parent_base_dir = parent_base_dir
        self.parent_package = parent_package

        if self.package is not None:
            if "_group_" in self.package:
                pkg = self.package
                resolved = pkg.replace("_group_", self.get_default_package())
                self.package = f"_global_.{resolved}"

    def is_optional(self) -> bool:
        raise NotImplementedError()

    def get_group_path(self) -> str:
        raise NotImplementedError()

    def get_config_path(self) -> str:
        raise NotImplementedError()

    def get_default_package(self) -> str:
        return self.get_group_path().replace("/", ".")

    def get_final_package(self, default_to_package_header: bool = True) -> str:
        """
        :param default_to_package_header: if package is not present, fallback to package header
        :return:
        """
        raise NotImplementedError()

    def _relative_group_path(self) -> str:
        raise NotImplementedError()

    def get_name(self) -> Optional[str]:
        raise NotImplementedError()

    def _get_attributes(self) -> List[str]:
        raise NotImplementedError()

    def _get_flags(self) -> List[str]:
        raise NotImplementedError()

    def _get_parent_package(self) -> Optional[str]:
        ret = self.__dict__["parent_package"]
        assert ret is None or isinstance(ret, str)
        return ret

    def is_virtual(self) -> bool:
        return False

    def is_deleted(self) -> bool:
        if "deleted" in self.__dict__:
            return bool(self.__dict__["deleted"])
        else:
            return False

    def set_package_header(self, package_header: Optional[str]) -> None:
        assert self.__dict__["package_header"] is None

        if package_header is None:
            return

        if not version.base_at_least("1.2"):
            if "_group_" in package_header or "_name_" in package_header:
                path = self.get_config_path()
                url = "https://hydra.cc/docs/1.2/upgrades/1.0_to_1.1/changes_to_package_header"
                deprecation_warning(
                    message=dedent(
                        f"""\
                        In '{path}': Usage of deprecated keyword in package header '# @package {package_header}'.
                        See {url} for more information"""
                    ),
                )

            if package_header == "_group_":
                return

        # package header is always interpreted as absolute.
        # if it does not have a _global_ prefix, add it.
        if package_header != "_global_" and not package_header.startswith("_global_."):
            if package_header == "":
                package_header = "_global_"
            else:
                package_header = f"_global_.{package_header}"

        if not version.base_at_least("1.2"):
            package_header = package_header.replace(
                "_group_", self.get_default_package()
            )
        self.__dict__["package_header"] = package_header

    def get_package_header(self) -> Optional[str]:
        ret = self.__dict__["package_header"]
        assert ret is None or isinstance(ret, str)
        return ret

    def get_package(self, default_to_package_header: bool = True) -> Optional[str]:
        if self.__dict__["package"] is None and default_to_package_header:
            ret = self.__dict__["package_header"]
        else:
            ret = self.__dict__["package"]
        assert ret is None or isinstance(ret, str)
        return ret

    def _get_final_package(
        self,
        parent_package: Optional[str],
        package: Optional[str],
        name: Optional[str],
    ) -> str:
        assert parent_package is not None

        if package is None:
            package = self._relative_group_path().replace("/", ".")

        if isinstance(name, str):
            # name computation should be deferred to after the final config group choice is done

            if not version.base_at_least("1.2"):
                if "_name_" in package:
                    package = package.replace("_name_", name)

        if parent_package == "":
            ret = package
        else:
            if package == "":
                ret = parent_package
            else:
                ret = f"{parent_package}.{package}"

        lgi = ret.rfind("_global_")
        if lgi == -1:
            return ret
        else:
            return ret[lgi + len("_global_") + 1 :]

    def __repr__(self) -> str:
        attrs = []
        attr_names = self._get_attributes()
        for attr in attr_names:
            value = getattr(self, attr)
            if value is not None:
                if isinstance(value, str):
                    svalue = f'"{value}"'
                else:
                    svalue = value
                attrs.append(f"{attr}={svalue}")

        flags = []
        flag_names = self._get_flags()
        for flag in flag_names:
            value = getattr(self, flag)
            if value:
                flags.append(f"{flag}=True")

        ret = f"{','.join(attrs)}"

        if len(flags) > 0:
            ret = f"{ret},{','.join(flags)}"
        return f"{type(self).__name__}({ret})"

    def is_interpolation(self) -> bool:
        raise NotImplementedError()

    def is_missing(self) -> bool:
        """
        True if the name of the config is '???'
        :return:
        """
        raise NotImplementedError()

    def resolve_interpolation(self, known_choices: DictConfig) -> None:
        raise NotImplementedError()

    def _resolve_interpolation_impl(
        self, known_choices: DictConfig, val: Optional[str]
    ) -> str:
        node = OmegaConf.create({"_dummy_": val})
        node._set_parent(known_choices)
        try:
            ret = node["_dummy_"]
            assert isinstance(ret, str)
            return ret
        except InterpolationResolutionError:
            options = [
                x
                for x in known_choices.keys()
                if x != "defaults" and isinstance(x, str)
            ]
            if len(options) > 0:
                options_str = ", ".join(options)
                msg = f"Error resolving interpolation '{val}', possible interpolation keys: {options_str}"
            else:
                msg = f"Error resolving interpolation '{val}'"
            raise ConfigCompositionException(msg)

    def get_override_key(self) -> str:
        default_pkg = self.get_default_package()
        final_pkg = self.get_final_package(default_to_package_header=False)
        key = self.get_group_path()
        if default_pkg != final_pkg:
            if final_pkg == "":
                final_pkg = "_global_"
            key = f"{key}@{final_pkg}"
        return key

    def get_relative_override_key(self) -> str:
        raise NotImplementedError()

    def is_override(self) -> bool:
        raise NotImplementedError()

    def is_external_append(self) -> bool:
        raise NotImplementedError()


@dataclass
class VirtualRoot(InputDefault):
    def is_virtual(self) -> bool:
        return True

    def is_self(self) -> bool:
        return False

    def is_optional(self) -> bool:
        raise NotImplementedError()

    def get_group_path(self) -> str:
        raise NotImplementedError()

    def get_config_path(self) -> str:
        return "<root>"

    def get_final_package(self, default_to_package_header: bool = True) -> str:
        raise NotImplementedError()

    def _relative_group_path(self) -> str:
        raise NotImplementedError()

    def get_name(self) -> str:
        raise NotImplementedError()

    def is_missing(self) -> bool:
        return False

    def _get_attributes(self) -> List[str]:
        raise NotImplementedError()

    def _get_flags(self) -> List[str]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "VirtualRoot()"

    def resolve_interpolation(self, known_choices: DictConfig) -> None:
        raise NotImplementedError()

    def is_override(self) -> bool:
        return False

    def is_external_append(self) -> bool:
        return False


@dataclass(repr=False)
class ConfigDefault(InputDefault):
    path: Optional[str] = None
    optional: bool = False
    deleted: Optional[bool] = None

    def __post_init__(self) -> None:
        if self.is_self() and self.package is not None:
            raise ValueError("_self_@PACKAGE is not supported")
        if self.package == "_here_":
            self.package = ""

    def is_self(self) -> bool:
        return self.path == "_self_"

    def is_optional(self) -> bool:
        return self.optional

    def get_group_path(self) -> str:
        assert self.parent_base_dir is not None
        assert self.path is not None

        if self.path.startswith("/"):
            path = self.path[1:]
            absolute = True
        else:
            path = self.path
            absolute = False

        idx = path.rfind("/")
        if idx == -1:
            group = ""
        else:
            group = path[0:idx]

        if not absolute:
            if self.parent_base_dir == "":
                return group
            else:
                if group == "":
                    return f"{self.parent_base_dir}"
                else:
                    return f"{self.parent_base_dir}/{group}"
        else:
            return group

    def get_name(self) -> Optional[str]:
        assert self.path is not None
        idx = self.path.rfind("/")
        if idx == -1:
            return self.path
        else:
            return self.path[idx + 1 :]

    def get_config_path(self) -> str:
        assert self.parent_base_dir is not None
        assert self.path is not None
        if self.path.startswith("/"):
            path = self.path[1:]
            absolute = True
        else:
            path = self.path
            absolute = False

        if not absolute:
            if self.parent_base_dir == "":
                return path
            else:
                return f"{self.parent_base_dir}/{path}"
        else:
            return path

    def get_final_package(self, default_to_package_header: bool = True) -> str:
        return self._get_final_package(
            self.parent_package,
            self.get_package(default_to_package_header),
            self.get_name(),
        )

    def _relative_group_path(self) -> str:
        assert self.path is not None
        if self.path.startswith("/"):
            path = self.path[1:]
        else:
            path = self.path

        idx = path.rfind("/")
        if idx == -1:
            return ""
        else:
            return path[0:idx]

    def _get_attributes(self) -> List[str]:
        return ["path", "package", "deleted"]

    def _get_flags(self) -> List[str]:
        return ["optional"]

    def is_interpolation(self) -> bool:
        path = self.get_config_path()
        node = AnyNode(path)
        return node._is_interpolation()

    def resolve_interpolation(self, known_choices: DictConfig) -> None:
        path = self.get_config_path()
        self.path = self._resolve_interpolation_impl(known_choices, path)

    def is_missing(self) -> bool:
        return self.get_name() == "???"

    def is_override(self) -> bool:
        return False

    def is_external_append(self) -> bool:
        return False


_legacy_interpolation_pattern: Pattern[str] = re.compile(r"\${defaults\.\d\.")


@dataclass(repr=False)
class GroupDefault(InputDefault):
    # config group name if present
    group: Optional[str] = None
    # config file name
    value: Optional[Union[str, List[str]]] = None
    optional: bool = False

    override: bool = False
    deleted: Optional[bool] = None

    config_name_overridden: bool = field(default=False, compare=False, repr=False)
    # True if this item was added using +foo=bar from the external overrides
    external_append: bool = field(default=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        assert self.group is not None and self.group != ""
        if self.package == "_here_":
            self.package = ""

    def is_self(self) -> bool:
        return self.value == "_self_"

    def is_optional(self) -> bool:
        return self.optional

    def is_override(self) -> bool:
        return self.override

    def get_group_path(self) -> str:
        assert self.parent_base_dir is not None
        assert self.group is not None

        if self.group.startswith("/"):
            group = self.group[1:]
            absolute = True
        else:
            group = self.group
            absolute = False

        if self.parent_base_dir == "" or absolute:
            return group
        else:
            return f"{self.parent_base_dir}/{group}"

    def get_config_path(self) -> str:
        group_path = self.get_group_path()
        assert group_path != ""

        return f"{group_path}/{self.get_name()}"

    def is_name(self) -> bool:
        return self.value is None or isinstance(self.value, str)

    def is_options(self) -> bool:
        return isinstance(self.value, list)

    def get_name(self) -> Optional[str]:
        assert self.value is None or isinstance(self.value, str)
        return self.value

    def get_options(self) -> List[str]:
        assert isinstance(self.value, list)
        return self.value

    def get_final_package(self, default_to_package_header: bool = True) -> str:
        name = self.get_name() if self.is_name() else None
        return self._get_final_package(
            self._get_parent_package(),
            self.get_package(default_to_package_header=default_to_package_header),
            name,
        )

    def _relative_group_path(self) -> str:
        assert self.group is not None
        if self.group.startswith("/"):
            return self.group[1:]
        else:
            return self.group

    def _get_attributes(self) -> List[str]:
        return ["group", "value", "package", "deleted"]

    def _get_flags(self) -> List[str]:
        return ["optional", "override"]

    def is_interpolation(self) -> bool:
        """
        True if config_name is an interpolation
        """
        if not self.is_name():
            return False

        name = self.get_name()
        if isinstance(name, str):
            node = AnyNode(name)
            return node._is_interpolation()
        else:
            return False

    def resolve_interpolation(self, known_choices: DictConfig) -> None:
        name = self.get_name()
        if name is not None:
            if re.match(_legacy_interpolation_pattern, name) is not None:
                msg = dedent(
                    f"""
Defaults list element '{self.get_override_key()}={name}' is using a deprecated interpolation form.
See http://hydra.cc/docs/1.1/upgrades/1.0_to_1.1/defaults_list_interpolation for migration information."""
                )
                if not version.base_at_least("1.2"):
                    deprecation_warning(
                        message=msg,
                    )
                else:
                    raise ConfigCompositionException(msg)

            self.value = self._resolve_interpolation_impl(known_choices, name)

    def is_missing(self) -> bool:
        if self.is_name():
            return self.get_name() == "???"
        else:
            return False

    def get_relative_override_key(self) -> str:
        assert self.group is not None
        default_pkg = self.get_default_package()
        key = self.group
        if default_pkg != self.get_package() and self.package is not None:
            key = f"{key}@{self.package}"
        return key

    def is_external_append(self) -> bool:
        return self.external_append


@dataclass
class DefaultsTreeNode:
    node: InputDefault
    children: Optional[List[Union["DefaultsTreeNode", InputDefault]]] = None

    parent: Optional["DefaultsTreeNode"] = field(
        default=None,
        repr=False,
        compare=False,
    )

    def parent_node(self) -> Optional[InputDefault]:
        if self.parent is None:
            return None
        else:
            return self.parent.node
