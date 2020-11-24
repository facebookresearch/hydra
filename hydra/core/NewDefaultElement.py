from dataclasses import dataclass, field
from typing import Optional


@dataclass
class InputDefault:
    def is_self(self) -> bool:
        raise NotImplementedError()

    def get_group_path(self) -> str:
        raise NotImplementedError()

    def get_config_path(self) -> str:
        raise NotImplementedError()


@dataclass
class ConfigDefault(InputDefault):
    path: str
    package: Optional[str] = None
    parent_base_dir: Optional[str] = field(default=None, compare=False, repr=False)

    def is_self(self) -> bool:
        return self.path == "_self_" or self.path.endswith("/_self_")

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

    def get_config_path(self) -> str:
        assert self.parent_base_dir is not None
        if self.parent_base_dir == "":
            return self.path
        else:
            return f"{self.parent_base_dir}/{self.path}"


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
