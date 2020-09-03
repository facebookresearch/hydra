# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import shutil
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

import requests
from omegaconf import MISSING, DictConfig, OmegaConf
from packaging.version import Version, parse

import hydra
from hydra.core.config_store import ConfigStore
from hydra.test_utils.test_utils import find_parent_dir_containing, get_run_output

log = logging.getLogger(__name__)


class Action(Enum):
    check = 1
    build = 2


@dataclass
class Config:
    action: Action = Action.check
    packages: List[str] = MISSING
    build_targets: Tuple[str, ...] = ("sdist", "bdist_wheel")
    build_dir: str = "build"


ConfigStore.instance().store(name="config", node=Config)


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
class Package:
    name: str
    local_version: Version
    latest_version: Version


def parse_version(ver: str) -> Version:
    v = parse(ver)
    assert isinstance(v, Version)
    return v


def get_package_info(path: str) -> Package:
    try:
        prev = os.getcwd()
        os.chdir(path)
        out, _err = get_run_output(cmd=[f"{path}/setup.py", "--version"])
        local_version: Version = parse_version(out)
        package_name, _err = get_run_output(cmd=[f"{path}/setup.py", "--name"])
    finally:
        os.chdir(prev)

    remote_metadata = get_metadata(package_name)
    latest = get_releases(remote_metadata)[-1]
    return Package(
        name=package_name, local_version=local_version, latest_version=latest
    )


def build_package(cfg: Config, pkg_path: str) -> None:
    try:
        prev = os.getcwd()
        os.chdir(pkg_path)
        log.info(f"Building {get_package_info('.').name}")
        shutil.rmtree("dist", ignore_errors=True)
        get_run_output(
            cmd=["setup.py", "build", *cfg.build_targets], allow_warnings=True
        )
    finally:
        os.chdir(prev)

    dist = f"{pkg_path}/dist"
    for file in os.listdir(dist):
        shutil.copy(src=f"{dist}/{file}", dst=cfg.build_dir)


@hydra.main(config_name="config")
def main(cfg: Config) -> None:
    hydra_root = find_parent_dir_containing(target="ATTRIBUTION")
    build_dir = f"{os.getcwd()}/{cfg.build_dir}"
    Path(build_dir).mkdir(parents=True)
    log.info(f"Build outputs : {build_dir}")
    if cfg.action == Action.check:
        log.info("Checking for eligible releases")
        for pkg_path in cfg.packages:
            pkg_path = os.path.normpath(os.path.join(hydra_root, pkg_path))
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
        log.info("Publishing eligible releases")
        for pkg_path in cfg.packages:
            pkg_path = os.path.normpath(os.path.join(hydra_root, pkg_path))
            ret = get_package_info(pkg_path)
            if ret.local_version > ret.latest_version:
                build_package(cfg, pkg_path)
    else:
        raise ValueError("Unexpected action type")


if __name__ == "__main__":
    main()
