import subprocess
import sys
from typing import List

import pytest


@pytest.mark.parametrize(
    "run_cmd",
    [
        pytest.param(["test-initialization-app", "module_installed"], id="run_as_app"),
        pytest.param(
            [sys.executable, "-m", "test_initialization_app.main", "module_installed"],
            id="run_as_module",
        ),
        pytest.param(
            [sys.executable, "test_initialization_app/main.py", "module_installed",],
            id="run_as_script",
        ),
    ],
)
def test_initialization_full_app_installed(run_cmd: List[str]) -> None:
    subprocess.check_call(run_cmd)
