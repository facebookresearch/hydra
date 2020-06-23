# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from typing import List

import pytest
from pytest import param


@pytest.mark.parametrize(
    "run_cmd",
    [
        param(["initialization-test-app", "module_installed"], id="run_as_app"),
        param(
            [sys.executable, "-m", "initialization_test_app.main", "module_installed"],
            id="run_as_module",
        ),
        param(
            [sys.executable, "initialization_test_app/main.py", "module_installed"],
            id="run_as_script",
        ),
    ],
)
def test_initialization_full_app_installed(run_cmd: List[str]) -> None:
    subprocess.check_call(run_cmd)
