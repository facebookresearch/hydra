# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys
import pytest
import re
import subprocess
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import chdir_hydra_root, verify_dir_outputs

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import task_runner, sweep_runner  # noqa: F401
from hydra.test_utils.test_utils import does_not_raise

chdir_hydra_root()


@pytest.mark.parametrize(
    "args,output_conf",
    [
        ([], OmegaConf.create()),
        (
            ["abc=123", "hello.a=456", "hello.b=5671"],
            OmegaConf.create(dict(abc=123, hello=dict(a=456, b=5671))),
        ),
    ],
)
def test_tutorial_simple_cli_app(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "examples/tutorial/1_simple_cli_app/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


def test_tutorial_working_directory(tmpdir):
    cmd = [
        sys.executable,
        "examples/tutorial/8_working_directory/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert result.decode("utf-8").rstrip() == "Working directory : {}".format(tmpdir)


@pytest.mark.parametrize(
    "args,expected",
    [
        ([], ["Info level message"]),
        (["hydra.verbose=[__main__]"], ["Info level message", "Debug level message"]),
    ],
)
def test_tutorial_logging(tmpdir, args, expected):
    cmd = [
        sys.executable,
        "examples/tutorial/9_logging/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    lines = result.decode("utf-8").splitlines()
    assert len(lines) == len(expected)
    for i in range(len(lines)):
        assert re.findall(expected[i], lines[i])


@pytest.mark.parametrize(
    "args,output_conf",
    [
        (
            [],
            OmegaConf.create(
                {"db": {"driver": "mysql", "pass": "secret", "user": "omry"}}
            ),
        )
    ],
)
def test_tutorial_config_file(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "examples/tutorial/2_config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            [],
            does_not_raise(
                OmegaConf.create(
                    {"db": {"driver": "mysql", "pass": "secret", "user": "omry"}}
                )
            ),
        ),
        (["dataset.path=abc"], pytest.raises(subprocess.CalledProcessError)),
    ],
)
def test_tutorial_config_file_bad_key(tmpdir, args, expected):
    """ Similar to the previous test, but also tests exception values"""
    with expected:
        cmd = [
            sys.executable,
            "examples/tutorial/2_config_file/my_app.py",
            "hydra.run.dir=" + str(tmpdir),
        ]
        cmd.extend(args)
        subprocess.check_output(cmd)


@pytest.mark.parametrize(
    "args,output_conf",
    [
        ([], OmegaConf.create()),
        (
            ["db=postgresql"],
            OmegaConf.create(
                {
                    "db": {
                        "driver": "postgresql",
                        "pass": "drowssap",
                        "timeout": 10,
                        "user": "postgre_user",
                    }
                }
            ),
        ),
    ],
)
def test_tutorial_config_groups(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "examples/tutorial/3_config_groups/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


@pytest.mark.parametrize(
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
def test_tutorial_defaults(tmpdir, args, expected):
    cmd = [
        sys.executable,
        "examples/tutorial/4_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == OmegaConf.create(expected)


@pytest.mark.parametrize(
    "args,output_conf",
    [
        (
            [],
            OmegaConf.create(
                {
                    "db": {
                        "class": "tutorial.objects_example.my_app.MySQLConnection",
                        "params": {
                            "host": "localhost",
                            "user": "root",
                            "password": 1234,
                        },
                    }
                }
            ),
        ),
        (
            ["db=postgresql"],
            OmegaConf.create(
                {
                    "db": {
                        "class": "tutorial.objects_example.my_app.MySQLConnection",
                        "params": {
                            "host": "localhost",
                            "user": "root",
                            "password": 1234,
                        },
                    }
                }
            ),
        ),
    ],
)
def test_objects_example(tmpdir, task_runner, args, output_conf):  # noqa: F811
    with task_runner(
        calling_file="examples/patterns/objects/my_app.py",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=[],
    ) as task:
        assert task.job_ret.cfg == output_conf
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


def test_composition_config_example(task_runner):  # noqa: F811
    with task_runner(
        calling_file="examples/tutorial/5_composition/my_app.py",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=["schema=school"],
    ) as task:
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


def test_sweeping_example(sweep_runner):  # noqa: F811
    with sweep_runner(
        calling_file="examples/tutorial/5_composition/my_app.py",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=["schema=warehouse,support", "db=mysql,postgresql"],
    ) as sweep:
        overrides = {
            ("schema=warehouse", "db=mysql"),
            ("schema=warehouse", "db=postgresql"),
            ("schema=support", "db=mysql"),
            ("schema=support", "db=postgresql"),
        }
        assert len(sweep.returns[0]) == 4
        for ret in sweep.returns[0]:
            assert tuple(ret.overrides) in overrides


def test_specializing_config_example(task_runner):  # noqa: F811
    with task_runner(
        calling_file="examples/patterns/specializing_config/example.py",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=["dataset=cifar10"],
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="cifar10", path="/datasets/cifar10"),
            model=dict(num_layers=5, type="alexnet"),
        )
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


@pytest.mark.parametrize(
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
def test_advanced_ad_hoc_composition(tmpdir, args, expected):
    cmd = [
        sys.executable,
        "examples/advanced/ad_hoc_composition/hydra_compose_example.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == OmegaConf.create(expected)
