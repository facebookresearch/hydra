# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from difflib import unified_diff
from pathlib import Path
from typing import Any

import pytest
from omegaconf import OmegaConf

from configen.config import ConfigenConf
from configen.configen import generate
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root(subdir="tools/configen")


conf: ConfigenConf = OmegaConf.structured(
    ConfigenConf(
        header="""# Compared against generated code
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# fmt: off
# isort:skip_file
# flake8: noqa"""
    )
)


@pytest.mark.parametrize(
    "module_name,class_name",
    [
        # pytest.param("tests.test_modules", "Empty", id="Empty"),
        pytest.param("tests.test_modules", "UntypedArg", id="UntypedArg"),
        pytest.param("tests.test_modules", "IntArg", id="IntArg"),
        pytest.param("tests.test_modules", "UnionArg", id="UnionArg"),
        pytest.param(
            "tests.test_modules", "WithLibraryClassArg", id="WithLibraryClassArg"
        ),
        pytest.param(
            "tests.test_modules",
            "IncompatibleDataclassArg",
            id="IncompatibleDataclassArg",
        ),
    ],
)
def test_generated_code(module_name: str, class_name: str) -> None:

    expected_file = (
        Path(module_name.replace(".", "/")) / "expected" / f"{class_name}.py"
    )
    expected = expected_file.read_text()

    generated = generate(cfg=conf, module_name=module_name, class_name=class_name)

    lines = [
        line
        for line in unified_diff(
            expected.splitlines(),
            generated.splitlines(),
            fromfile=str(expected_file),
            tofile="Generated",
        )
    ]

    diff = "\n".join(lines)
    if generated != expected:
        print(diff)
        assert False, f"Mismatch between {expected_file} and generated code"


def test_example_application(monkeypatch: Any, tmpdir: Path):
    cmd = [
        sys.executable,
        "example/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        "user.params.name=Batman",
    ]
    # a little hack: the examples are not installed as a part of configen.
    result = subprocess.check_output(cmd)
    assert result.decode("utf-8").strip() == "User: name=Batman, age=7"
