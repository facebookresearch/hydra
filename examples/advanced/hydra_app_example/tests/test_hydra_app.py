# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
The following tests are testing that the app actually runs as expected
when installed and executed from the command line.
You don't need to repeat those tests in your own app.
"""
import subprocess
import sys
import unittest
from typing import List

import pytest

from hydra.core.global_hydra import GlobalHydra
from hydra.experimental import compose, initialize_with_module
from hydra_app.main import add

# A few notes about this example:
# 1. We use initialize_with_module(). Hydra will find the config relative to the module.
# 2. This is not sensitive to the working directory.
# 3. Your config directory should be importable, it need to have a __init__.py (can be empty).
# 4. If you want to initialize Hydra more than once you need to clear the GlobalHydra singleton.


def test_generated_config() -> None:
    try:
        # config is relative to a module
        initialize_with_module(calling_module="hydra_app.main", config_path="conf")
        cfg = compose(config_name="config", overrides=["app.user=test_user"])
        assert cfg == {
            "app": {"user": "test_user", "num1": 10, "num2": 20},
            "db": {"host": "localhost", "port": 3306},
        }
    finally:
        GlobalHydra.instance().clear()


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
    try:
        initialize_with_module(calling_module="hydra_app.main", config_path="conf")
        cfg = compose(config_name="config", overrides=overrides)
        assert add(cfg.app, "num1", "num2") == expected
    finally:
        GlobalHydra.instance().clear()


# Some unittest style tests for good measure (pytest runs them)
class TestWithUnittest(unittest.TestCase):
    def test_generated_config(self) -> None:
        try:
            # config is relative to a module
            initialize_with_module(calling_module="hydra_app.main", config_path="conf")
            cfg = compose(config_name="config", overrides=["app.user=test_user"])
            assert cfg == {
                "app": {"user": "test_user", "num1": 10, "num2": 20},
                "db": {"host": "localhost", "port": 3306},
            }
        finally:
            GlobalHydra.instance().clear()


# Tests ensuring the app is runnable as a script and as a console script.
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
