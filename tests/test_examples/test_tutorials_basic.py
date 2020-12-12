# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import subprocess
from pathlib import Path
from typing import Any, List

import pytest
from _pytest.python_api import RaisesContext
from omegaconf import DictConfig, OmegaConf

from hydra.test_utils.test_utils import (
    TSweepRunner,
    TTaskRunner,
    chdir_hydra_root,
    get_run_output,
    verify_dir_outputs,
)

chdir_hydra_root()


@pytest.mark.parametrize(  # type: ignore
    "args,output_conf",
    [
        ([], OmegaConf.create()),
        (
            ["+db.driver=mysql", "+db.user=omry", "+db.password=secret"],
            OmegaConf.create(
                {"db": {"driver": "mysql", "user": "omry", "password": "secret"}}
            ),
        ),
    ],
)
def test_tutorial_simple_cli_app(
    tmpdir: Path, args: List[str], output_conf: DictConfig
) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/1_simple_cli/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == output_conf


def test_tutorial_working_directory(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/basic/running_your_hydra_app/3_working_directory/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert result == "Working directory : {}".format(tmpdir)


@pytest.mark.parametrize(  # type: ignore
    "args,expected",
    [
        ([], ["Info level message"]),
        (["hydra.verbose=[__main__]"], ["Info level message", "Debug level message"]),
    ],
)
def test_tutorial_logging(tmpdir: Path, args: List[str], expected: List[str]) -> None:
    cmd = [
        "examples/tutorials/basic/running_your_hydra_app/4_logging/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result, _err = get_run_output(cmd)
    lines = result.splitlines()
    assert len(lines) == len(expected)
    for i in range(len(lines)):
        assert re.findall(re.escape(expected[i]), lines[i])


@pytest.mark.parametrize(  # type: ignore
    "args,output_conf",
    [
        (
            [],
            OmegaConf.create(
                {"db": {"driver": "mysql", "password": "secret", "user": "omry"}}
            ),
        )
    ],
)
def test_tutorial_config_file(tmpdir: Path, args: List[str], output_conf: Any) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == output_conf


@pytest.mark.parametrize(  # type: ignore
    "args,expected",
    [
        (
            [],
            OmegaConf.create(
                {"db": {"driver": "mysql", "user": "omry", "password": "secret"}}
            ),
        ),
        (["dataset.path=abc"], pytest.raises(subprocess.CalledProcessError)),
    ],
)
def test_tutorial_config_file_bad_key(
    tmpdir: Path, args: List[str], expected: Any
) -> None:
    """ Similar to the previous test, but also tests exception values"""

    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    if isinstance(expected, RaisesContext):
        with expected:
            get_run_output(cmd, print_stderr=False)
    else:
        stdout, _stderr = get_run_output(cmd)
        assert OmegaConf.create(stdout) == expected


@pytest.mark.parametrize(  # type: ignore
    "args,output_conf",
    [
        ([], OmegaConf.create()),
        (
            ["+db=postgresql"],
            OmegaConf.create(
                {
                    "db": {
                        "driver": "postgresql",
                        "password": "drowssap",
                        "timeout": 10,
                        "user": "postgre_user",
                    }
                }
            ),
        ),
    ],
)
def test_tutorial_config_groups(
    tmpdir: Path, args: List[str], output_conf: DictConfig
) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/4_config_groups/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == output_conf


@pytest.mark.parametrize(  # type: ignore
    "args,expected",
    [
        ([], {"db": {"driver": "mysql", "pass": "secret", "user": "omry"}}),
        (
            ["db=postgresql"],
            {
                "db": {
                    "driver": "postgresql",
                    "pass": "drowssap",
                    "timeout": 10,
                    "user": "postgre_user",
                }
            },
        ),
        (
            ["db=postgresql", "db.timeout=20"],
            {
                "db": {
                    "driver": "postgresql",
                    "pass": "drowssap",
                    "timeout": 20,
                    "user": "postgre_user",
                }
            },
        ),
    ],
)
def test_tutorial_defaults(tmpdir: Path, args: List[str], expected: DictConfig) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/5_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == OmegaConf.create(expected)


def test_composition_config_example(
    hydra_restore_singletons: Any, hydra_task_runner: TTaskRunner
) -> None:
    with hydra_task_runner(
        calling_file="examples/tutorials/basic/your_first_hydra_app/6_composition/my_app.py",
        calling_module=None,
        config_path="conf",
        config_name="config.yaml",
        overrides=["schema=school"],
        configure_logging=True,
    ) as task:
        assert task.job_ret is not None
        assert task.job_ret.cfg == {
            "db": {"driver": "mysql", "user": "omry", "pass": "secret"},
            "ui": {"windows": {"create_db": True, "view": True}},
            "schema": {
                "database": "school",
                "tables": [
                    {
                        "name": "students",
                        "fields": [{"name": "string"}, {"class": "int"}],
                    },
                    {
                        "name": "exams",
                        "fields": [
                            {"profession": "string"},
                            {"time": "data"},
                            {"class": "int"},
                        ],
                    },
                ],
            },
        }
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


def test_sweeping_example(
    hydra_restore_singletons: Any, hydra_sweep_runner: TSweepRunner
) -> None:
    with hydra_sweep_runner(
        calling_file="examples/tutorials/basic/your_first_hydra_app/6_composition/my_app.py",
        calling_module=None,
        config_path="conf",
        config_name="config.yaml",
        task_function=None,
        overrides=["schema=warehouse,support", "db=mysql,postgresql"],
    ) as sweep:
        overrides = {
            ("schema=warehouse", "db=mysql"),
            ("schema=warehouse", "db=postgresql"),
            ("schema=support", "db=mysql"),
            ("schema=support", "db=postgresql"),
        }

        assert sweep.returns is not None and len(sweep.returns[0]) == 4
        for ret in sweep.returns[0]:
            assert tuple(ret.overrides) in overrides


@pytest.mark.parametrize(  # type: ignore
    "args,expected",
    [
        (
            [],
            {
                "db": {"driver": "mysql", "pass": "secret", "user": "${env:USER}"},
                "ui": {"windows": {"create_db": True, "view": True}},
                "schema": {
                    "database": "school",
                    "tables": [
                        {
                            "name": "students",
                            "fields": [{"name": "string"}, {"class": "int"}],
                        },
                        {
                            "name": "exams",
                            "fields": [
                                {"profession": "string"},
                                {"time": "data"},
                                {"class": "int"},
                            ],
                        },
                    ],
                },
            },
        )
    ],
)
def test_advanced_ad_hoc_composition(
    monkeypatch: Any, tmpdir: Path, args: List[str], expected: Any
) -> None:

    monkeypatch.setenv("USER", "test_user")
    cmd = [
        "examples/advanced/ad_hoc_composition/hydra_compose_example.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == OmegaConf.create(expected)


def test_examples_using_the_config_object(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/3_using_config/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]

    get_run_output(cmd)
