# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import re
import shutil
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Tuple

import hydra
import requests
from hydra.core.config_store import ConfigStore
from hydra.test_utils.test_utils import find_parent_dir_containing, run_python_script
from omegaconf import II, MISSING, SI, DictConfig, OmegaConf
from packaging.version import Version, parse

log = logging.getLogger(__name__)


class Action(Enum):
    check = 1
    build = 2
    bump = 3


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


ConfigStore.instance().store(name="config_schema", node=Config)


@lru_cache()
def get_metadata(package_name: str) -> DictConfig:
    url = f"https://pypi.org/pypi/{package_name}/json"
    with requests.get(url, timeout=10) as response:
        ret = OmegaConf.create(response.content.decode("utf-8"))
    response.close()
    assert isinstance(ret, DictConfig)
    return ret


def get_releases(metadata: DictConfig) -> List[Version]:
    ret: List[Version] = []
    for ver, files in metadata.releases.items():
        for file in files:
            if file.packagetype == "bdist_wheel" and file.yanked is not True:
                v = parse_version(ver)
                ret.append(v)
    return sorted(ret)


@dataclass
class PackageInfo:
    name: str
    local_version: Version
    latest_version: Version


def parse_version(ver: str) -> Version:
    v = parse(ver)
    assert isinstance(v, Version)
    return v


def get_package_info(path: str) -> PackageInfo:
    try:
        prev = os.getcwd()
        path = os.path.abspath(path)
        os.chdir(path)
        out, _err = run_python_script(
            cmd=[f"{path}/setup.py", "--version"], allow_warnings=True
        )
        local_version: Version = parse_version(out)
        package_name, _err = run_python_script(
            cmd=[f"{path}/setup.py", "--name"], allow_warnings=True
        )
    finally:
        os.chdir(prev)

    remote_metadata = get_metadata(package_name)
    latest = get_releases(remote_metadata)[-1]
    return PackageInfo(
        name=package_name, local_version=local_version, latest_version=latest
    )


def build_package(cfg: Config, pkg_path: str, build_dir: str) -> None:
    try:
        prev = os.getcwd()
        os.chdir(pkg_path)
        log.info(f"Building {get_package_info('.').name}")
        shutil.rmtree("dist", ignore_errors=True)
        cmd = ["-m", "build", "-o", build_dir, *cfg.build_targets]
        run_python_script(
            cmd=cmd,
            allow_warnings=False,
        )
    finally:
        os.chdir(prev)


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


def bump_version_in_file(cfg: Config, name: str, ver_file: Path) -> None:
    loaded = ver_file.read_text("utf-8")
    # https://regex101.com/r/DoxaSI/1
    regex = r"((?:__)?version(?:__)?\s*=\s*)((?:\"|\')(.*?)(?:\"|\'))"

    matches = re.search(regex, loaded)

    if matches:
        new_version = _next_version(matches.group(3))
        log.info(f"Bumping version of {name} from {matches.group(2)} to {new_version}")
        subst = f'{matches.group(1)}"{new_version}"'
        result = re.sub(regex, subst, loaded, 0)
        if not cfg.dry_run:
            ver_file.write_text(result)
    else:
        raise ValueError(f"Could not find version in {ver_file}")


def bump_version(cfg: Config, package: Package, hydra_root: str) -> None:
    if package.version_type == VersionType.SETUP:
        ver_file = Path(hydra_root) / package.path / "setup.py"
        bump_version_in_file(cfg, package.name, ver_file)
    elif package.version_type == VersionType.FILE:
        ver_file = Path(hydra_root) / package.path / package.version_file
        bump_version_in_file(cfg, package.name, ver_file)
    else:
        raise ValueError()


OmegaConf.register_new_resolver("parent_key", lambda _parent_: _parent_._key())


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: Config) -> None:
    hydra_root = find_parent_dir_containing(target="ATTRIBUTION")
    build_dir = f"{os.getcwd()}/{cfg.build_dir}"
    Path(build_dir).mkdir(parents=True)
    log.info(f"Build outputs : {build_dir}")
    if cfg.action == Action.check:
        log.info("Checking for unpublished packages")
        for package in cfg.packages.values():
            pkg_path = os.path.normpath(os.path.join(hydra_root, package.path))
            ret = get_package_info(pkg_path)
            if ret.local_version == ret.latest_version:
                log.info(f"\U0000274a : {ret.name} : match ({ret.latest_version})")
            elif ret.local_version > ret.latest_version:
                log.info(
                    f"\U0000274b : {ret.name} : newer (local={ret.local_version} > latest={ret.latest_version})"
                )
            else:
                log.info(
                    f"\U0000274c : {ret.name} : older (local={ret.local_version} < latest={ret.latest_version})"
                )
    elif cfg.action == Action.build:
        log.info("Building unpublished packages")
        for package in cfg.packages.values():
            pkg_path = os.path.normpath(os.path.join(hydra_root, package.path))
            ret = get_package_info(pkg_path)
            if ret.local_version > ret.latest_version:
                build_package(cfg, pkg_path, build_dir)
    elif cfg.action == Action.bump:
        log.info("Bumping version of published packages")
        for package in cfg.packages.values():
            pkg_path = os.path.normpath(os.path.join(hydra_root, package.path))
            ret = get_package_info(pkg_path)
            if ret.local_version == ret.latest_version:
                bump_version(cfg, package, hydra_root)

    else:
        raise ValueError("Unexpected action type")


if __name__ == "__main__":
    main()
