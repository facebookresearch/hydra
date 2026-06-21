# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from tools.release.release import (
    DevReleasePackageInfo,
    LocalPackageInfo,
    PackageInfo,
    fail_if_any_target_version_published,
    format_dev_release_package_table,
    is_publishable,
    parse_version,
    validate_dev_version,
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


def test_validate_dev_version_accepts_dev_version() -> None:
    validate_dev_version(parse_version("1.4.0.dev3"))


def test_validate_dev_version_rejects_non_dev_version() -> None:
    with pytest.raises(
        ValueError,
        match="Dev releases require a \\.devN version; got 1.4.0",
    ):
        validate_dev_version(parse_version("1.4.0"))


def test_format_dev_release_package_table_includes_publish_plan() -> None:
    table = format_dev_release_package_table(
        [
            DevReleasePackageInfo(
                name="hydra-core",
                local_version=parse_version("1.4.0.dev2"),
                target_version=parse_version("1.4.0.dev3"),
                latest_version=parse_version("1.4.0.dev2"),
                target_version_published=False,
            )
        ]
    )

    assert "Package" in table
    assert "Current local version" in table
    assert "Target version" in table
    assert "PyPI status" in table
    assert "hydra-core" in table
    assert "1.4.0.dev2" in table
    assert "1.4.0.dev3" in table
    assert "not published" in table


def test_fail_if_any_target_version_published_rejects_published_package() -> None:
    infos = [
        DevReleasePackageInfo(
            name="hydra-core",
            local_version=parse_version("1.4.0.dev2"),
            target_version=parse_version("1.4.0.dev3"),
            latest_version=parse_version("1.4.0.dev3"),
            target_version_published=True,
        )
    ]

    with pytest.raises(
        ValueError,
        match="Target version is already published for selected packages: hydra-core",
    ):
        fail_if_any_target_version_published(infos)
