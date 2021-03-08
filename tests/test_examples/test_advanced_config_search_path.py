# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path

from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root, run_python_script

chdir_hydra_root()


def test_config_search_path(tmpdir: Path) -> None:
    cmd = [
        "examples/advanced/config_search_path/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = run_python_script(cmd)
    assert OmegaConf.create(result) == {
        "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
    }
