# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from contextlib import nullcontext

import pytest

from tools.release import release
from tools.release.release import (
    DevReleasePackageInfo,
    LocalPackageInfo,
    Package,
    PackageInfo,
    fail_if_any_target_version_published,
    filter_packages,
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


def test_filter_packages_keeps_requested_packages_in_order() -> None:
    packages = {
        "hydra": Package(path="."),
        "hydra_optuna_sweeper": Package(path="plugins/hydra_optuna_sweeper"),
        "hydra_ray_launcher": Package(path="plugins/hydra_ray_launcher"),
    }

    selected = filter_packages(packages, " hydra_ray_launcher, hydra_optuna_sweeper ")

    assert list(selected) == ["hydra_ray_launcher", "hydra_optuna_sweeper"]


def test_filter_packages_rejects_unknown_packages() -> None:
    packages = {
        "hydra": Package(path="."),
        "hydra_optuna_sweeper": Package(path="plugins/hydra_optuna_sweeper"),
    }

    with pytest.raises(
        ValueError,
        match=(
            "Unknown package filter: hydra_rq_launcher. "
            "Available packages in selected set: hydra, hydra_optuna_sweeper"
        ),
    ):
        filter_packages(packages, "hydra_rq_launcher")


def test_dispatch_publish_workflow_uses_json_boolean_input(monkeypatch) -> None:
    calls = []

    def fake_run_checked(cmd, cwd=None, stdin=None):
        calls.append((cmd, cwd, stdin))
        return ""

    monkeypatch.setattr(release, "_run_checked", fake_run_checked)
    monkeypatch.setattr(
        release,
        "get_remote_url",
        lambda hydra_root, vcs: "https://github.com/facebookresearch/hydra",
    )

    release.dispatch_publish_workflow(
        "/repo",
        "sl",
        "hydra-full-release",
        parse_version("1.4.0.dev3"),
        "main",
        "hydra_optuna_sweeper",
    )

    assert calls == [
        (
            [
                "gh",
                "workflow",
                "run",
                "publish.yml",
                "--repo",
                "facebookresearch/hydra",
                "--ref",
                "main",
                "--json",
            ],
            "/repo",
            '{"package_set": "hydra-full-release", '
            '"expected_version": "1.4.0.dev3", "publish": "true", '
            '"only": "hydra_optuna_sweeper"}',
        )
    ]


def test_check_build_artifacts_upgrades_smoke_environment_pip(
    monkeypatch, tmp_path
) -> None:
    wheel = tmp_path / "package.whl"
    wheel.touch()
    smoke_dir = tmp_path / "smoke"
    calls = []

    def fake_run_checked(cmd, cwd=None, stdin=None):
        calls.append(cmd)
        return ""

    monkeypatch.setattr(release, "_run_checked", fake_run_checked)
    monkeypatch.setattr(
        release.tempfile,
        "TemporaryDirectory",
        lambda prefix: nullcontext(str(smoke_dir)),
    )

    release.check_build_artifacts(tmp_path)

    venv_path = smoke_dir / "venv"
    smoke_python = release._python_bin(venv_path)
    assert calls == [
        [release.sys.executable, "-m", "twine", "check", str(wheel)],
        [release.sys.executable, "-m", "venv", str(venv_path)],
        [str(smoke_python), "-m", "pip", "install", "--upgrade", "pip"],
        [str(smoke_python), "-m", "pip", "install", "--no-deps", str(wheel)],
    ]


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        (
            "https://github.com/facebookresearch/hydra",
            "https://github.com/facebookresearch/hydra",
        ),
        (
            "default = https://github.com/facebookresearch/hydra",
            "https://github.com/facebookresearch/hydra",
        ),
    ],
)
def test_get_remote_url_accepts_sapling_path_output_formats(
    monkeypatch, output, expected
) -> None:
    monkeypatch.setattr(release, "_single_line", lambda cmd, cwd: output)

    assert release.get_remote_url("/repo", "sl") == expected


@pytest.mark.parametrize(
    "remote_url",
    [
        "https://github.com/facebookresearch/hydra",
        "https://github.com/facebookresearch/hydra.git",
        "ssh://git@github.com/facebookresearch/hydra",
        "ssh://git@github.com/facebookresearch/hydra.git",
        "git@github.com:facebookresearch/hydra.git",
    ],
)
def test_get_github_repo_slug_accepts_common_github_remote_urls(remote_url) -> None:
    assert release.get_github_repo_slug(remote_url) == "facebookresearch/hydra"
