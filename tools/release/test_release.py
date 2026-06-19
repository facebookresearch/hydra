# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from tools.release.release import (
    LocalPackageInfo,
    PackageInfo,
    is_publishable,
    parse_version,
    validate_local_version,
)


def test_publishable_when_local_version_is_older_than_latest_but_unpublished() -> None:
    info = PackageInfo(
        name="hydra-core",
        local_version=parse_version("1.3.5"),
        latest_version=parse_version("1.4.0"),
        local_version_published=False,
    )

    assert is_publishable(info)


def test_not_publishable_when_local_version_is_already_published() -> None:
    info = PackageInfo(
        name="hydra-core",
        local_version=parse_version("1.3.5"),
        latest_version=parse_version("1.4.0"),
        local_version_published=True,
    )

    assert not is_publishable(info)


def test_validate_local_version_accepts_expected_version() -> None:
    info = LocalPackageInfo(name="hydra-core", local_version=parse_version("1.4.0"))

    validate_local_version(info, parse_version("1.4.0"))


def test_validate_local_version_rejects_unexpected_version() -> None:
    info = LocalPackageInfo(name="hydra-core", local_version=parse_version("1.4.0"))

    with pytest.raises(
        ValueError,
        match="hydra-core version is 1.4.0; expected 1.4.1",
    ):
        validate_local_version(info, parse_version("1.4.1"))
