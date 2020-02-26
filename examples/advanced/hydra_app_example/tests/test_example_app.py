# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
The following tests are testing that the app actually runs as expected
when installed and executed from the command line.
You don't need to repeat those tests in your own app.
"""
import subprocess
import sys
from typing import Any

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root, does_not_raise

chdir_hydra_root()


def verify_output(result: bytes) -> None:
    assert OmegaConf.create(str(result.decode("utf-8"))) == OmegaConf.create(
        dict(dataset=dict(name="imagenet", path="/datasets/imagenet"))
    )


def test_python_run() -> None:
    verify_output(
        subprocess.check_output(
            [sys.executable, "examples/advanced/hydra_app_example/hydra_app/main.py"]
        )
    )


def test_installed_run() -> None:
    verify_output(subprocess.check_output(["hydra_app"]))


@pytest.mark.parametrize("env_key", ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE"])  # type: ignore
@pytest.mark.parametrize(  # type: ignore
    "env_value, expectation",
    [("bad_module", pytest.raises(Exception)), ("hydra_app.main", does_not_raise())],
)
def test_installed_run_with_env_module_override(
    env_key: str, env_value: str, expectation: Any
) -> None:
    verify_output(subprocess.check_output(["hydra_app"]))
