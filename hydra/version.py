# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

# Source of truth for Hydra's version

import re
from textwrap import dedent
from typing import Any, Optional, Tuple

from . import __version__
from ._internal.deprecation_warning import deprecation_warning
from .core.singleton import Singleton
from .errors import HydraException

_UNSPECIFIED_: Any = object()

__compat_version__ = "1.1"

_VERSION_PATTERN = re.compile(
    r"(?P<major>[0-9]+)\.(?P<minor>[0-9]+)"
    r"(?:\.[0-9]+(?:rc[0-9]+|\.dev[0-9]+)?)?"
)


class VersionBase(metaclass=Singleton):
    def __init__(self) -> None:
        self.version_base: Optional[str] = _UNSPECIFIED_

    def setbase(self, version: str) -> None:
        assert isinstance(version, str), f"Unexpected Version type : {type(version)}"
        self.version_base = version

    def getbase(self) -> Optional[str]:
        return self.version_base

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "VersionBase":
        return Singleton.instance(VersionBase, *args, **kwargs)  # type: ignore

    @staticmethod
    def set_instance(instance: "VersionBase") -> None:
        assert isinstance(instance, VersionBase)
        Singleton._instances[VersionBase] = instance  # type: ignore


def _parse_version(ver: str) -> Tuple[int, int]:
    if not isinstance(ver, str):
        raise TypeError(f"Expected version string, got {type(ver).__name__}")

    match = _VERSION_PATTERN.fullmatch(ver)
    if match is None:
        raise ValueError(f"Invalid version: {ver!r}")

    return int(match.group("major")), int(match.group("minor"))


def _get_version(ver: str) -> str:
    major, minor = _parse_version(ver)
    return f"{major}.{minor}"


def base_at_least(ver: str) -> bool:
    _version_base = VersionBase.instance().getbase()
    if type(_version_base) is type(_UNSPECIFIED_):
        VersionBase.instance().setbase(__compat_version__)
        _version_base = __compat_version__
    assert isinstance(_version_base, str)
    return _parse_version(_version_base) >= _parse_version(ver)


def getbase() -> Optional[str]:
    return VersionBase.instance().getbase()


def setbase(ver: Any) -> None:
    """
    Set the `version_base` parameter, which is used to support backward compatibility
    with older versions of Hydra.
    """
    if type(ver) is type(_UNSPECIFIED_):
        deprecation_warning(
            message=dedent(f"""
            The version_base parameter is not specified.
            Please specify a compatibility version level, or None.
            Will assume defaults for version {__compat_version__}"""),
            stacklevel=3,
        )
        _version_base = __compat_version__
    elif ver is None:
        _version_base = _get_version(__version__)
    else:
        _version_base = _get_version(ver)
        if _parse_version(_version_base) < _parse_version(__compat_version__):
            raise HydraException(f'version_base must be >= "{__compat_version__}"')
    VersionBase.instance().setbase(_version_base)
