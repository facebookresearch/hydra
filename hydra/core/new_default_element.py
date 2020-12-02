# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class ResultDefault:
    config_path: Optional[str] = None
    parent: Optional[str] = None
    package: Optional[str] = None
    is_self: bool = False

    def __repr__(self) -> str:
        attrs = []
        attr_names = "config_path", "package", "parent"
        for attr in attr_names:
            value = getattr(self, attr)
            if value is not None:
                attrs.append(f'{attr}="{value}"')

        flags = []
        flag_names = ["is_self"]
        for flag in flag_names:
            value = getattr(self, flag)
            if value:
                flags.append(f"{flag}=True")

        ret = f"{','.join(attrs + flags)}"
        return f"{type(self).__name__}({ret})"


@dataclass
class InputDefault:

    parent_base_dir: Optional[str] = field(default=None, compare=False, repr=False)
    parent_package: Optional[str] = field(default=None, compare=False, repr=False)
    package_header: Optional[str] = field(default=None, compare=False)

    def is_self(self) -> bool:
        raise NotImplementedError()

    def get_group_path(self) -> str:
        raise NotImplementedError()

    def get_config_path(self) -> str:
        raise NotImplementedError()

    def get_default_package(self) -> str:
        return self.get_group_path().replace("/", ".")

    def get_final_package(self) -> str:
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

    def set_package_header(self, package_header: str) -> None:
        assert self.__dict__["package_header"] is None
        # package header is always interpreted as absolute.
        # if it does not have a _global_ prefix, add it.
        if package_header != "_global_" and not package_header.startswith("_global_."):
            if package_header == "":
                package_header = "_global_"
            else:
                package_header = f"_global_.{package_header}"
        self.__dict__["package_header"] = package_header

    def get_package_header(self) -> Optional[str]:
        ret = self.__dict__["package_header"]
        assert ret is None or isinstance(ret, str)
        return ret

    def get_package(self) -> Optional[str]:
        if self.__dict__["package"] is None:
            ret = self.__dict__["package_header"]
        else:
            ret = self.__dict__["package"]
        assert ret is None or isinstance(ret, str)
        return ret

    def _get_final_package(
        self,
        parent_package: Optional[str],
        package: Optional[str],
        name: str,
    ) -> str:
        assert parent_package is not None
        if package is None:
            package = self._relative_group_path().replace("/", ".")

        if name is not None:
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

    def get_override_key(self) -> str:
        default_pkg = self.get_default_package()
        final_pkg = self.get_final_package()
        key = self.get_group_path()
        if default_pkg != final_pkg:
            key = f"{key}@{final_pkg}"
        return key

    def __repr__(self) -> str:
        attrs = []
        attr_names = self._get_attributes()
        for attr in attr_names:
            value = getattr(self, attr)
            if value is not None:
                attrs.append(f'{attr}="{value}"')

        flags = []
        flag_names = self._get_flags()
        for flag in flag_names:
            value = getattr(self, flag)
            if value:
                flags.append(f"{flag}=True")

        ret = f"{','.join(attrs)}"

        if len(flags) > 0:
            ret = f"{ret} ({','.join(flags)})"
        return f"{type(self).__name__}({ret})"


@dataclass
class VirtualRoot(InputDefault):
    def is_virtual(self) -> bool:
        return True

    def is_self(self) -> bool:
        raise NotImplementedError()

    def get_group_path(self) -> str:
        raise NotImplementedError()

    def get_config_path(self) -> str:
        return "<root>"

    def get_default_package(self) -> str:
        return self.get_group_path().replace("/", ".")

    def get_final_package(self) -> str:
        raise NotImplementedError()

    def _relative_group_path(self) -> str:
        raise NotImplementedError()

    def get_name(self) -> str:
        raise NotImplementedError()

    def _get_attributes(self) -> List[str]:
        raise NotImplementedError()

    def _get_flags(self) -> List[str]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "VirtualRoot()"


@dataclass(repr=False)
class ConfigDefault(InputDefault):
    path: Optional[str] = None
    package: Optional[str] = None

    def __post_init__(self) -> None:
        if self.is_self() and self.package is not None:
            raise ValueError("_self_@PACKAGE is not supported")
        if self.package == "_here_":
            self.package = ""

    def is_self(self) -> bool:
        return self.path == "_self_"

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

    def get_final_package(self) -> str:
        return self._get_final_package(
            self.parent_package, self.get_package(), self.get_name()
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
        return ["path", "package"]

    def _get_flags(self) -> List[str]:
        return []


@dataclass(repr=False)
class GroupDefault(InputDefault):
    # config group name if present
    group: Optional[str] = None
    # config file name
    name: Optional[str] = None
    optional: bool = False
    package: Optional[str] = None

    override: bool = False

    config_name_overridden: bool = field(default=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        assert self.group is not None and self.group != ""
        if self.package == "_here_":
            self.package = ""

    def is_self(self) -> bool:
        return self.name == "_self_"

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

    def get_name(self) -> Optional[str]:
        return self.name

    def get_final_package(self) -> str:
        return self._get_final_package(
            self._get_parent_package(), self.get_package(), self.get_name()
        )

    def _relative_group_path(self) -> str:
        assert self.group is not None
        if self.group.startswith("/"):
            return self.group[1:]
        else:
            return self.group

    def _get_attributes(self) -> List[str]:
        return ["group", "name", "package"]

    def _get_flags(self) -> List[str]:
        return ["optional", "override"]


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
