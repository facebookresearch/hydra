# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
import unittest
from typing import List

import pytest

from hydra.experimental import compose, initialize, initialize_config_module
from hydra_app.main import add


def test_with_initialize_config_module_ctx() -> None:
    # 1. initialize_with_module_ctx will add the config module to the config search path within the context
    # 2. The module with your configs should be importable. it needs to have a __init__.py (can be empty).
    # 3. The module should be absolute (not realative to this file)
    # 4. This approach is not sensitive to the location of this file.
    with initialize_config_module(config_module="hydra_app.conf"):
        # config is relative to a module
        cfg = compose(config_name="config", overrides=["app.user=test_user"])
        assert cfg == {
            "app": {"user": "test_user", "num1": 10, "num2": 20},
            "db": {"host": "localhost", "port": 3306},
        }


def test_with_initialize_ctx() -> None:
    # 1. initialize will add config_path the config search path within the context
    # 2. The module with your configs should be importable. it needs to have a __init__.py (can be empty).
    # 3. THe config path is relative to the file calling initialize (control this with caller_stack_depth)
    # 4. This approach IS sensitive to the location of this file.
    with initialize(config_path="../hydra_app/conf"):
        # config is relative to a module
        cfg = compose(config_name="config", overrides=["app.user=test_user"])
        assert cfg == {
            "app": {"user": "test_user", "num1": 10, "num2": 20},
            "db": {"host": "localhost", "port": 3306},
        }


# Testing app logic with different config combinations
@pytest.mark.parametrize(  # type: ignore
    "overrides, expected",
    [
        (["app.user=test_user"], 30),
        (["app.user=test_user", "app.num1=20", "app.num2=100"], 120),
        (["app.user=test_user", "app.num1=-1001", "app.num2=1000"], -1),
    ],
)
def test_user_logic(overrides: List[str], expected: int) -> None:
    with initialize_config_module(config_module="hydra_app.conf"):
        cfg = compose(config_name="config", overrides=overrides)
        assert add(cfg.app, "num1", "num2") == expected


# Some unittest style tests for good measure (pytest runs them)
class TestWithUnittest(unittest.TestCase):
    def test_generated_config(self) -> None:
        with initialize_config_module(config_module="hydra_app.conf"):
            cfg = compose(config_name="config", overrides=["app.user=test_user"])
            assert cfg == {
                "app": {"user": "test_user", "num1": 10, "num2": 20},
                "db": {"host": "localhost", "port": 3306},
            }


# The following tests are testing that the app actually runs as expected
# when installed and executed from the command line.
# You don't need to repeat those tests in your own app.
class TestAppOutput:

    # Testing the Hydra app as an executable script
    # This only works if we are at the root of the hydra-app-example
    def test_python_run(self, tmpdir: str) -> None:
        self.verify_output(
            subprocess.check_output(
                [
                    sys.executable,
                    "hydra_app/main.py",
                    f"hydra.run.dir={tmpdir}",
                    "app.user=test_user",
                ]
            )
        )

    # Testing the Hydra app as a console script
    def test_installed_run(self, tmpdir: str) -> None:
        self.verify_output(
            subprocess.check_output(
                ["hydra_app", f"hydra.run.dir={tmpdir}", "app.user=test_user"]
            )
        )

    @staticmethod
    def verify_output(result: bytes) -> None:
        assert str(result.decode("utf-8")).strip() == "Hello test_user, 10 + 20 = 30"
