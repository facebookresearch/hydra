# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

# Source of truth for Hydra's version

import warnings
from textwrap import dedent
from typing import Any, Optional

from packaging.version import Version

from . import __version__
from .core.singleton import Singleton
from .errors import Hydra14MigrationWarning, HydraException

_UNSPECIFIED_: Any = object()

__compat_version__: Version = Version("1.1")
_HYDRA_1_4_PREPARATION_GUIDE = (
    "https://hydra.cc/docs/upgrades/1.3_to_1.4/prepare_for_1_4/"
)


class VersionBase(metaclass=Singleton):
    def __init__(self) -> None:
        self.version_base: Optional[Version] = _UNSPECIFIED_

    def setbase(self, version: "Version") -> None:
        assert isinstance(
            version, Version
        ), f"Unexpected Version type : {type(version)}"
        self.version_base = version

    def getbase(self) -> Optional[Version]:
        return self.version_base

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "VersionBase":
        return Singleton.instance(VersionBase, *args, **kwargs)  # type: ignore

    @staticmethod
    def set_instance(instance: "VersionBase") -> None:
        assert isinstance(instance, VersionBase)
        Singleton._instances[VersionBase] = instance  # type: ignore


def _get_version(ver: str) -> Version:
    # Only consider major.minor as packaging will compare "1.2.0.dev2" < "1.2"
    pver = Version(ver)
    return Version(f"{pver.major}.{pver.minor}")


def base_at_least(ver: str) -> bool:
    _version_base = VersionBase.instance().getbase()
    if type(_version_base) is type(_UNSPECIFIED_):
        VersionBase.instance().setbase(__compat_version__)
        _version_base = __compat_version__
    assert isinstance(_version_base, Version)
    return _version_base >= _get_version(ver)


def getbase() -> Optional[Version]:
    return VersionBase.instance().getbase()


def setbase(ver: Any) -> None:
    if type(ver) is type(_UNSPECIFIED_):
        warnings.warn(
            dedent(
                f"""
            The version_base parameter is not specified.
            Hydra will assume defaults for version {__compat_version__}.
            Hydra 1.4 will remove this compatibility behavior.
            Before upgrading to Hydra 1.4, set version_base="1.3" and test your application.
            See {_HYDRA_1_4_PREPARATION_GUIDE} for preparation instructions."""
            ),
            category=Hydra14MigrationWarning,
            stacklevel=3,
        )
        _version_base = __compat_version__
    elif ver is None:
        _version_base = _get_version(__version__)
    else:
        _version_base = _get_version(ver)
        if _version_base < __compat_version__:
            raise HydraException(f'version_base must be >= "{__compat_version__}"')
        if _version_base == __compat_version__:
            warnings.warn(
                dedent(
                    f"""
                version_base="{_version_base}" selects Hydra 1.1 compatibility behavior.
                Hydra 1.4 will remove this compatibility behavior.
                Before upgrading to Hydra 1.4, set version_base="1.3" and test your application.
                See {_HYDRA_1_4_PREPARATION_GUIDE} for preparation instructions."""
                ),
                category=Hydra14MigrationWarning,
                stacklevel=3,
            )
    VersionBase.instance().setbase(_version_base)
