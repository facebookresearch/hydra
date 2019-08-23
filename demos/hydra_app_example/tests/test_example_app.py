import subprocess
import sys

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root, does_not_raise

chdir_hydra_root()


def verify_output(result):
    assert OmegaConf.create(str(result.decode("utf-8"))) == OmegaConf.create(
        dict(dataset=dict(name="imagenet", path="/datasets/imagenet"))
    )


def test_python_run():
    verify_output(
        subprocess.check_output(
            [sys.executable, "demos/hydra_app_example/hydra_app/main.py"]
        )
    )


def test_installed_run():
    verify_output(subprocess.check_output(["hydra_app"]))


@pytest.mark.parametrize("env_key", ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE"])
@pytest.mark.parametrize(
    "env_value, expectation",
    [("bad_module", pytest.raises(Exception)), ("hydra_app.main", does_not_raise())],
)
def test_installed_run_with_env_module_override(env_key, env_value, expectation):
    verify_output(subprocess.check_output(["hydra_app"]))
