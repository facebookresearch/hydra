import subprocess
import sys

from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root

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
