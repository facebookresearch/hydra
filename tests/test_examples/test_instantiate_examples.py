# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from textwrap import dedent
from typing import Any, List

import pytest

from hydra.test_utils.test_utils import (
    assert_text_same,
    chdir_hydra_root,
    get_run_output,
)

chdir_hydra_root()


@pytest.mark.parametrize(  # type: ignore
    "overrides,output",
    [
        ([], "MySQL connecting to localhost"),
        (["db=postgresql"], "PostgreSQL connecting to localhost"),
    ],
)
def test_instantiate_object(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], output: str
) -> None:
    monkeypatch.chdir("examples/instantiate/object")
    cmd = ["my_app.py", "hydra.run.dir=" + str(tmpdir)] + overrides
    result, _err = get_run_output(cmd)
    assert result == output


@pytest.mark.parametrize(  # type: ignore
    "overrides,output",
    [
        ([], "Driver : James Bond, 4 wheels"),
        (
            ["car.wheels=[{_target_:my_app.Wheel,radius:7,width:1}]"],
            "Driver : James Bond, 1 wheels",
        ),
    ],
)
def test_instantiate_object_recursive(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], output: str
) -> None:
    monkeypatch.chdir("examples/instantiate/object_recursive")
    cmd = ["my_app.py", "hydra.run.dir=" + str(tmpdir)] + overrides
    result, _err = get_run_output(cmd)
    assert result == output


@pytest.mark.parametrize(  # type: ignore
    "overrides,output",
    [
        ([], "MySQL connecting to localhost"),
        (["db=postgresql"], "PostgreSQL connecting to localhost"),
    ],
)
def test_instantiate_schema(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], output: str
) -> None:
    monkeypatch.chdir("examples/instantiate/schema")
    cmd = ["my_app.py", "hydra.run.dir=" + str(tmpdir)] + overrides
    result, _err = get_run_output(cmd)
    assert result == output


@pytest.mark.parametrize(  # type: ignore
    "overrides,expected",
    [
        (
            [],
            dedent(
                """\
                root(1)
                  left(20)
                    right(30)
                      left(400)
                      right(300)
                """
            ),
        ),
    ],
)
def test_instantiate_schema_recursive(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], expected: str
) -> None:
    monkeypatch.chdir("examples/instantiate/schema_recursive")
    cmd = ["my_app.py", "hydra.run.dir=" + str(tmpdir)] + overrides
    result, _err = get_run_output(cmd)
    assert_text_same(result, expected)


@pytest.mark.parametrize(  # type: ignore
    "overrides,expected",
    [
        (
            [],
            dedent(
                """\
                Optimizer(algo=SGD,lr=0.01)
                Optimizer(algo=SGD,lr=0.2)
                Trainer(
                  optimizer=Optimizer(algo=SGD,lr=0.01),
                  dataset=Dataset(name=Imagenet, path=/datasets/imagenet)
                )
                Trainer(
                  optimizer=Optimizer(algo=SGD,lr=0.3),
                  dataset=Dataset(name=cifar10, path=/datasets/cifar10)
                )
                Trainer(
                  optimizer={'_target_': 'my_app.Optimizer', 'algo': 'SGD', 'lr': 0.01},
                  dataset={'_target_': 'my_app.Dataset', 'name': 'Imagenet', 'path': '/datasets/imagenet'}
                )
                """
            ),
        ),
    ],
)
def test_instantiate_docs_example(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], expected: str
) -> None:
    monkeypatch.chdir("examples/instantiate/docs_example")
    cmd = ["my_app.py", "hydra.run.dir=" + str(tmpdir)] + overrides
    result, _err = get_run_output(cmd)
    assert_text_same(result, expected)
