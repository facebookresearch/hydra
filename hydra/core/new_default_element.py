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

    def set_package_header(self, package_header: str) -> None:
        assert self.__dict__["package_header"] is None
        # TODO: is package header relative or absolute?
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


@dataclass
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


@dataclass
class GroupDefault(InputDefault):
    # config group name if present
    group: Optional[str] = None
    # config file name
    name: Optional[str] = None
    optional: bool = False
    package: Optional[str] = None

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
