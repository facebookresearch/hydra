# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import re
import shutil
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import hydra
import requests  # type: ignore[import-untyped]
from hydra.core.config_store import ConfigStore
from hydra.test_utils.test_utils import find_parent_dir_containing, run_python_script
from omegaconf import II, MISSING, SI, DictConfig, OmegaConf
from packaging.version import Version, parse

log = logging.getLogger(__name__)


class Action(Enum):
    check = 1
    build = 2
    bump = 3
    set_version = 4


class BuildPolicy(Enum):
    unpublished = 1
    all = 2


class Repository(Enum):
    pypi = 1
    testpypi = 2


class VersionType(Enum):
    SETUP = 1
    FILE = 2


@dataclass
class Package:
    name: str = II("parent_key:")
    module: str = II(".name")
    path: str = MISSING
    version_type: VersionType = VersionType.FILE
    version_file: str = SI("${.module}/__init__.py")


@dataclass
class Config:
    dry_run: bool = False
    action: Action = Action.check
    packages: Dict[str, Package] = MISSING
    build_targets: Tuple[str, ...] = ("--sdist", "--wheel")
    build_dir: str = "build"
    build_policy: BuildPolicy = BuildPolicy.unpublished
    clean_build_dir: bool = False
    repository: Repository = Repository.pypi
    require_artifacts: bool = False
    version: Optional[str] = None


ConfigStore.instance().store(name="config_schema", node=Config)


@lru_cache()
def get_metadata(repository: Repository, package_name: str) -> Optional[DictConfig]:
    host = {
        Repository.pypi: "pypi.org",
        Repository.testpypi: "test.pypi.org",
    }[repository]
    url = f"https://{host}/pypi/{package_name}/json"
    with requests.get(url, timeout=10) as response:
        if response.status_code == 404:
            return None
        response.raise_for_status()
        ret = OmegaConf.create(response.content.decode("utf-8"))
    response.close()
    assert isinstance(ret, DictConfig)
    return ret


def get_latest_release(metadata: Optional[DictConfig]) -> Optional[Version]:
    if metadata is None:
        return None
    ret: List[Version] = []
    for ver, files in metadata.releases.items():
        for file in files:
            if file.packagetype == "bdist_wheel" and file.yanked is not True:
                v = parse_version(ver)
                ret.append(v)
    if len(ret) == 0:
        return None
    return sorted(ret)[-1]


@dataclass
class PackageInfo:
    name: str
    local_version: Version
    latest_version: Optional[Version]


@dataclass
class LocalPackageInfo:
    name: str
    local_version: Version


def parse_version(ver: str) -> Version:
    v = parse(ver)
    assert isinstance(v, Version)
    return v


def _last_output_line(out: str) -> str:
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Expected command output")
    return lines[-1]


def get_local_package_info(path: str) -> LocalPackageInfo:
    try:
        prev = os.getcwd()
        path = os.path.abspath(path)
        os.chdir(path)
        out, _err = run_python_script(
            cmd=[f"{path}/setup.py", "--version"], allow_warnings=True
        )
        package_name, _err = run_python_script(
            cmd=[f"{path}/setup.py", "--name"], allow_warnings=True
        )
    finally:
        os.chdir(prev)

    return LocalPackageInfo(
        name=_last_output_line(package_name),
        local_version=parse_version(_last_output_line(out)),
    )


def get_package_info(repository: Repository, path: str) -> PackageInfo:
    local = get_local_package_info(path)
    remote_metadata = get_metadata(repository, local.name)
    latest = get_latest_release(remote_metadata)
    return PackageInfo(
        name=local.name, local_version=local.local_version, latest_version=latest
    )


def is_publishable(info: PackageInfo) -> bool:
    return info.latest_version is None or info.local_version > info.latest_version


def format_latest_version(version: Optional[Version]) -> str:
    if version is None:
        return "<not published>"
    return str(version)


def build_package(cfg: Config, pkg_path: str, build_dir: str) -> None:
    try:
        prev = os.getcwd()
        os.chdir(pkg_path)
        local = get_local_package_info(".")
        log.info(f"Building {local.name} ({local.local_version})")
        shutil.rmtree("dist", ignore_errors=True)
        cmd = ["-m", "build", "-o", build_dir, *cfg.build_targets]
        run_python_script(
            cmd=cmd,
            allow_warnings=False,
        )
    finally:
        os.chdir(prev)


def prepare_build_dir(cfg: Config, build_dir_path: Path) -> None:
    if cfg.clean_build_dir and build_dir_path.exists():
        shutil.rmtree(build_dir_path)
    elif build_dir_path.exists() and any(build_dir_path.iterdir()):
        raise ValueError(
            f"Build directory {build_dir_path} is not empty. "
            "Use clean_build_dir=true or choose an empty build_dir."
        )
    build_dir_path.mkdir(parents=True, exist_ok=True)


def _next_version(version: str) -> str:
    cur = parse(version)
    assert isinstance(cur, Version)
    if cur.is_devrelease:
        prefix = "dev"
        assert cur.dev is not None
        num = cur.dev + 1
        new_version = f"{cur.major}.{cur.minor}.{cur.micro}.{prefix}{num}"
    elif cur.is_prerelease:
        assert cur.pre is not None
        prefix = cur.pre[0]
        num = cur.pre[1] + 1
        new_version = f"{cur.major}.{cur.minor}.{cur.micro}.{prefix}{num}"
    elif cur.is_postrelease:
        assert cur.post is not None
        num = cur.post + 1
        new_version = f"{cur.major}.{cur.minor}.{cur.micro}.{num}"
    else:
        micro = cur.micro + 1
        new_version = f"{cur.major}.{cur.minor}.{micro}"

    return str(new_version)


def bump_version_in_file(
    cfg: Config, name: str, ver_file: Path, target_version: Optional[str] = None
) -> None:
    loaded = ver_file.read_text("utf-8")
    # https://regex101.com/r/DoxaSI/1
    regex = r"((?:__)?version(?:__)?\s*=\s*)((?:\"|\')(.*?)(?:\"|\'))"

    matches = re.search(regex, loaded)

    if matches:
        new_version = target_version or _next_version(matches.group(3))
        parse_version(new_version)
        log.info(f"Setting version of {name} from {matches.group(3)} to {new_version}")
        subst = f'{matches.group(1)}"{new_version}"'
        result = re.sub(regex, subst, loaded, count=0)
        if not cfg.dry_run:
            ver_file.write_text(result)
    else:
        raise ValueError(f"Could not find version in {ver_file}")


def bump_version(
    cfg: Config,
    package: Package,
    hydra_root: str,
    target_version: Optional[str] = None,
) -> None:
    if package.version_type == VersionType.SETUP:
        ver_file = Path(hydra_root) / package.path / "setup.py"
        bump_version_in_file(cfg, package.name, ver_file, target_version)
    elif package.version_type == VersionType.FILE:
        ver_file = Path(hydra_root) / package.path / package.version_file
        bump_version_in_file(cfg, package.name, ver_file, target_version)
    else:
        raise ValueError()


OmegaConf.register_new_resolver("parent_key", lambda _parent_: _parent_._key())


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: Config) -> None:
    hydra_root = find_parent_dir_containing(target="ATTRIBUTION")
    build_dir_path = Path(cfg.build_dir).expanduser()
    if not build_dir_path.is_absolute():
        build_dir_path = Path(os.getcwd()) / build_dir_path
    if cfg.action == Action.build:
        prepare_build_dir(cfg, build_dir_path)
    else:
        build_dir_path.mkdir(parents=True, exist_ok=True)
    build_dir = str(build_dir_path)
    log.info(f"Build outputs : {build_dir}")
    if cfg.action == Action.check:
        log.info(f"Checking for unpublished packages on {cfg.repository.name}")
        for package in cfg.packages.values():
            pkg_path = os.path.normpath(os.path.join(hydra_root, package.path))
            ret = get_package_info(cfg.repository, pkg_path)
            if ret.local_version == ret.latest_version:
                log.info(f"\U0000274a : {ret.name} : match ({ret.latest_version})")
            elif is_publishable(ret):
                log.info(
                    f"\U0000274b : {ret.name} : newer (local={ret.local_version} > latest={format_latest_version(ret.latest_version)})"
                )
            else:
                log.info(
                    f"\U0000274c : {ret.name} : older (local={ret.local_version} < latest={ret.latest_version})"
                )
    elif cfg.action == Action.build:
        log.info(
            f"Building packages with policy {cfg.build_policy.name} against {cfg.repository.name}"
        )
        built_any = False
        for package in cfg.packages.values():
            pkg_path = os.path.normpath(os.path.join(hydra_root, package.path))
            if cfg.build_policy == BuildPolicy.all:
                build_package(cfg, pkg_path, build_dir)
                built_any = True
            else:
                ret = get_package_info(cfg.repository, pkg_path)
                if is_publishable(ret):
                    build_package(cfg, pkg_path, build_dir)
                    built_any = True
                else:
                    log.info(
                        f"Skipping {ret.name} ({ret.local_version}); latest on {cfg.repository.name} is {ret.latest_version}"
                    )
        if cfg.require_artifacts and not built_any:
            raise ValueError(
                f"No publishable artifacts were built for {cfg.repository.name}"
            )
    elif cfg.action == Action.bump:
        log.info(f"Bumping version of packages published on {cfg.repository.name}")
        for package in cfg.packages.values():
            pkg_path = os.path.normpath(os.path.join(hydra_root, package.path))
            ret = get_package_info(cfg.repository, pkg_path)
            if ret.local_version == ret.latest_version:
                bump_version(cfg, package, hydra_root)
    elif cfg.action == Action.set_version:
        if cfg.version is None:
            raise ValueError("action=set_version requires version=<target version>")
        parse_version(cfg.version)
        log.info(f"Setting package versions to {cfg.version}")
        for package in cfg.packages.values():
            bump_version(cfg, package, hydra_root, target_version=cfg.version)

    else:
        raise ValueError("Unexpected action type")


if __name__ == "__main__":
    main()
