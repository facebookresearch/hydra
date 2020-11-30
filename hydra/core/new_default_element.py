from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class ResultDefault:
    config_path: Optional[str] = None
    parent: Optional[str] = None
    package: Optional[str] = None
    is_self: bool = False


@dataclass
class InputDefault:
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

    def get_name(self) -> str:
        raise NotImplementedError()

    def _get_attributes(self) -> List[str]:
        raise NotImplementedError()

    def _get_flags(self) -> List[str]:
        raise NotImplementedError()

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
        return self.__dict__["package_header"]

    def get_package(self) -> str:
        if self.__dict__["package"] is None:
            return self.__dict__["package_header"]
        else:
            return self.__dict__["package"]

    def _get_final_package(
        self,
        parent_package: Optional[str],
        package: Optional[str],
        name: str,
    ) -> str:
        assert parent_package is not None
        if package is None:
            package = self._relative_group_path().replace("/", ".")

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


@dataclass(repr=False)
class ConfigDefault(InputDefault):
    path: str
    package: Optional[str] = None

    parent_base_dir: Optional[str] = field(default=None, compare=False, repr=False)
    parent_package: Optional[str] = field(default=None, compare=False, repr=False)
    package_header: Optional[str] = field(default=None, compare=False)

    def __post_init__(self):
        if self.is_self() and self.package is not None:
            raise ValueError("_self_@PACKAGE is not supported")

    def is_self(self) -> bool:
        return self.path == "_self_"

    def get_group_path(self) -> str:
        assert self.parent_base_dir is not None
        idx = self.path.rfind("/")
        if idx == -1:
            group = ""
        else:
            group = self.path[0:idx]

        if self.parent_base_dir == "":
            return group
        else:
            if group == "":
                return f"{self.parent_base_dir}"
            else:
                return f"{self.parent_base_dir}/{group}"

    def get_name(self) -> str:
        idx = self.path.rfind("/")
        if idx == -1:
            return self.path
        else:
            return self.path[idx + 1 :]

    def get_config_path(self) -> str:
        assert self.parent_base_dir is not None
        if self.parent_base_dir == "":
            return self.path
        else:
            return f"{self.parent_base_dir}/{self.path}"

    def get_final_package(self) -> str:
        return self._get_final_package(
            self.parent_package, self.get_package(), self.get_name()
        )

    def _relative_group_path(self) -> str:
        idx = self.path.rfind("/")
        if idx == -1:
            return ""
        else:
            return self.path[0:idx]

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

    parent_base_dir: Optional[str] = field(default=None, compare=False, repr=False)
    config_name_overridden: bool = field(default=False, compare=False, repr=False)
    package_header: Optional[str] = field(default=None, compare=False)

    def __post_init__(self):
        assert self.group is not None and self.group != ""

    def is_self(self) -> bool:
        return self.name == "_self_"

    def get_group_path(self) -> str:
        assert self.parent_base_dir is not None
        assert self.group is not None
        if self.parent_base_dir == "":
            return self.group
        else:
            return f"{self.parent_base_dir}/{self.group}"

    def get_config_path(self) -> str:
        group_path = self.get_group_path()
        assert group_path != ""

        return f"{group_path}/{self.name}"

    def get_name(self) -> str:
        return self.name

    def get_final_package(self) -> str:
        return self._get_final_package(
            self.parent_package, self.get_package(), self.get_name()
        )

    def _relative_group_path(self) -> str:
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
