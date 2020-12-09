# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path

from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root, get_run_output

chdir_hydra_root()


def test_advanced_package_override_simple(tmpdir: Path) -> None:
    cmd = [
        "examples/advanced/package_overrides/simple.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == {
        "db": {"driver": "mysql", "user": "omry", "pass": "secret"}
    }


def test_advanced_package_override_two_packages(tmpdir: Path) -> None:
    cmd = [
        "examples/advanced/package_overrides/two_packages.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == {
        "source": {"driver": "mysql", "user": "omry", "pass": "secret"},
        "destination": {"driver": "mysql", "user": "omry", "pass": "secret"},
    }
