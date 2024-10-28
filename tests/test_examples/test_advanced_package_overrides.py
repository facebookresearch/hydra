# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path

from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root, run_python_script

chdir_hydra_root()


def test_advanced_package_override_simple(tmpdir: Path) -> None:
    cmd = [
        "examples/advanced/package_overrides/simple.py",
        f'hydra.run.dir="{str(tmpdir)}"',
        "hydra.job.chdir=True",
    ]
    result, _err = run_python_script(cmd)
    assert OmegaConf.create(result) == {
        "db": {"driver": "mysql", "user": "omry", "pass": "secret"}
    }


def test_advanced_package_override_two_packages(tmpdir: Path) -> None:
    cmd = [
        "examples/advanced/package_overrides/two_packages.py",
        f'hydra.run.dir="{str(tmpdir)}"',
        "hydra.job.chdir=True",
    ]
    result, _err = run_python_script(cmd)
    assert OmegaConf.create(result) == {
        "source": {"driver": "mysql", "user": "omry", "pass": "secret"},
        "destination": {"driver": "mysql", "user": "omry", "pass": "secret"},
    }
