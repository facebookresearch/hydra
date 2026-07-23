# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pytest import MonkeyPatch

from hydra import compose, initialize_config_dir
from hydra.test_utils.test_utils import chdir_hydra_root, run_python_script

chdir_hydra_root()


def test_nested_defaults_list(tmpdir: Path) -> None:
    result, stderr = run_python_script(
        [
            "examples/advanced/nested_defaults_list/my_app.py",
            f'hydra.run.dir="{tmpdir}"',
            "hydra.job.chdir=True",
        ]
    )

    assert stderr == ""
    assert OmegaConf.create(result) == {
        "server": {"db": {"name": "mysql"}, "name": "apache"},
        "debug": False,
    }


def test_ray_example_config(
    hydra_restore_singletons: Any, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setenv("SELF_WARNING_AS_ERROR", "1")
    config_dir = Path("examples/advanced/ray_example/conf").absolute()
    with initialize_config_dir(version_base=None, config_dir=str(config_dir)):
        cfg = compose(config_name="config")

    assert cfg == {
        "dataset": {"name": "imagenet", "path": "/datasets/imagenet"},
        "model": {"type": "alexnet", "num_layers": 7},
        "ray": {"init": {"num_cpus": 4}},
    }
