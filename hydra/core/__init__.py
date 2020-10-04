# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import warnings
from dataclasses import dataclass
from textwrap import dedent
from typing import Optional, Pattern

from omegaconf import MISSING, AnyNode, DictConfig, OmegaConf

_legacy_interpolation_pattern: Pattern[str] = re.compile(r"\${defaults\.\d\.")


@dataclass
class DefaultElement:
    config_name: str
    config_group: Optional[str] = None
    optional: bool = False
    package: Optional[str] = None

    parent: Optional[str] = None

    # used in package rename
    rename_package_to: Optional[str] = None

    # True for default elements that are from overrides.
    # Those have somewhat different semantics
    from_override: bool = False

    # set to True for external overrides with +
    is_add: bool = False

    # is a delete indicator, used as input
    is_delete: bool = False

    # is this default deleted? used as output
    is_deleted: bool = False

    # True for the primary config (the one in compose() or @hydra.main())
    primary: bool = False

    skip_load: bool = False
    skip_load_reason: str = ""

    # If loaded, the search path it was loaded from
    search_path: str = MISSING

    def config_path(self) -> str:
        assert self.config_name is not None
        if self.config_group is not None:
            return f"{self.config_group}/{self.config_name}"
        else:
            return self.config_name

    def fully_qualified_group_name(self) -> Optional[str]:
        if self.config_group is None:
            return None
        if self.package is not None:
            return f"{self.config_group}@{self.package}"
        else:
            return f"{self.config_group}"

    def __repr__(self) -> str:
        package = self.package
        if self.is_package_rename():
            if self.package is not None:
                package = f"{self.package}:{self.rename_package_to}"
            else:
                package = f":{self.rename_package_to}"

        if self.config_group is None:
            if package is not None:
                ret = f"@{package}={self.config_name}"
            else:
                ret = f"{self.config_name}"
        else:
            if package is not None:
                ret = f"{self.config_group}@{package}={self.config_name}"
            else:
                ret = f"{self.config_group}={self.config_name}"

        if self.is_add:
            ret = f"+{ret}"
        if self.is_delete:
            ret = f"~{ret}"

        if self.parent is not None:
            ret = f"{ret} (parent:{self.parent})"

        flags = []
        flag_names = [
            "primary",
            "is_delete",
            "is_deleted",
            "optional",
            "from_override",
            "is_add",
        ]
        for flag in flag_names:
            if getattr(self, flag):
                flags.append(flag)

        if self.skip_load:
            flags.append(f"skip-load:{self.skip_load_reason}")

        if len(flags) > 0:
            ret = f"{ret} ({','.join(flags)})"

        return ret

    def is_package_rename(self) -> bool:
        return self.rename_package_to is not None

    def get_subject_package(self) -> Optional[str]:
        return (
            self.package if self.rename_package_to is None else self.rename_package_to
        )

    def is_interpolation(self) -> bool:
        """
        True if config_name is an interpolation
        """
        if isinstance(self.config_name, str):
            node = AnyNode(self.config_name)
            return node._is_interpolation()
        else:
            return False

    def resolve_interpolation(self, group_to_choice: DictConfig) -> None:
        assert self.config_group is not None
        if self.config_name is not None:
            if re.match(_legacy_interpolation_pattern, self.config_name) is not None:
                msg = dedent(
                    f"""
            Defaults list element '{self.fully_qualified_group_name()}={self.config_name}' \
is using a deprecated interpolation form.
            See http://hydra.cc/docs/next/upgrades/1.0_to_1.1/defaults_list_interpolation for migration information.
            """
                )
                warnings.warn(
                    category=UserWarning,
                    message=msg,
                )
        node = OmegaConf.create({self.config_group: self.config_name})
        node._set_parent(group_to_choice)
        self.config_name = node[self.config_group]

    def set_skip_load(self, reason: str) -> None:
        self.skip_load = True
        self.skip_load_reason = reason
