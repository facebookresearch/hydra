# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys

import pytest
import re
import subprocess
from omegaconf import OmegaConf

from hydra.test_utils.launcher_common_tests import (
    sweep_1_job,
    sweep_2_jobs,
    not_sweeping_hydra_overrides,
    sweep_two_config_groups,
)
from hydra.test_utils.test_utils import chdir_hydra_root, verify_dir_outputs

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import task_runner, sweep_runner  # noqa: F401

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
        "tutorial/simple_cli_app/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


def test_tutorial_working_directory(tmpdir):
    cmd = [
        sys.executable,
        "tutorial/working_directory/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert result.decode("utf-8").rstrip() == "Working directory : {}".format(tmpdir)


@pytest.mark.parametrize(
    "args,expected",
    [
        ([], ["Info level message"]),
        (["-v" "__main__"], ["Info level message", "Debug level message"]),
    ],
)
def test_tutorial_logging(tmpdir, args, expected):
    cmd = [sys.executable, "tutorial/logging/my_app.py", "hydra.run.dir=" + str(tmpdir)]
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
        ),
        (
            ["dataset.path=abc"],
            OmegaConf.create(
                {
                    "dataset": {"path": "abc"},
                    "db": {"driver": "mysql", "pass": "secret", "user": "omry"},
                }
            ),
        ),
    ],
)
def test_tutorial_config_file(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "tutorial/config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


@pytest.mark.parametrize(
    "args,output_conf",
    [
        (
            [],
            OmegaConf.create(
                {
                    "dataset": {"name": "imagenet", "path": "/datasets/imagenet"},
                    "optimizer": {"lr": 0.001, "type": "nesterov"},
                }
            ),
        ),
        (
            ["dataset.path=foo"],
            OmegaConf.create(
                {
                    "dataset": {"name": "imagenet", "path": "foo"},
                    "optimizer": {"lr": 0.001, "type": "nesterov"},
                }
            ),
        ),
    ],
)
def test_demo_4_config_splitting(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "demos/4_config_splitting/experiment.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


@pytest.mark.parametrize(
    "args,output_conf",
    [
        (
            [],
            OmegaConf.create(
                {
                    "optimizer": {"lr": 0.001, "type": "nesterov"},
                    "dataset": {"name": "imagenet", "path": "/datasets/imagenet"},
                }
            ),
        ),
        (
            ["optimizer=adam"],
            OmegaConf.create(
                {
                    "optimizer": {"beta": 0.01, "lr": 0.1, "type": "adam"},
                    "dataset": {"name": "imagenet", "path": "/datasets/imagenet"},
                }
            ),
        ),
    ],
)
def test_demo_5_config_groups(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "demos/5_config_groups/defaults.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


def test_fairtask_sweep_1_job(sweep_runner):  # noqa: F811
    sweep_1_job(sweep_runner, overrides=["hydra/launcher=basic"])


def test_fairtask_sweep_2_jobs(sweep_runner):  # noqa: F811
    sweep_2_jobs(sweep_runner, overrides=["hydra/launcher=basic"])


def test_not_sweeping_hydra_overrides(sweep_runner):  # noqa: F811
    not_sweeping_hydra_overrides(sweep_runner, overrides=["hydra/launcher=basic"])


def test_fairtask_sweep_1_job_strict(sweep_runner):  # noqa: F811
    sweep_1_job(sweep_runner, strict=True, overrides=["hydra/launcher=basic"])


def test_fairtask_sweep_1_job_strict_and_bad_key(sweep_runner):  # noqa: F811
    with pytest.raises(KeyError):
        sweep_1_job(
            sweep_runner,
            strict=True,
            overrides=["hydra/launcher=basic", "hydra.foo=bar"],
        )


def test_fairtask_sweep_2_optimizers(sweep_runner):  # noqa: F811
    sweep_two_config_groups(sweep_runner, overrides=["hydra/launcher=basic"])


def test_specializing_configs_demo(task_runner):  # noqa: F811
    with task_runner(
        calling_file="demos/8_specializing_config/example.py",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=["dataset=cifar10"],
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="cifar10", path="/datasets/cifar10"),
            model=dict(num_layers=5, type="alexnet"),
        )
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


def test_short_module_name(tmpdir):
    try:
        os.chdir("tutorial/config_file")
        cmd = [sys.executable, "my_app.py", "hydra.run.dir=" + str(tmpdir)]
        modified_env = os.environ.copy()
        modified_env["HYDRA_MAIN_MODULE"] = "my_app"
        result = subprocess.check_output(cmd, env=modified_env)
        assert OmegaConf.create(str(result.decode("utf-8"))) == {
            "db": {"driver": "mysql", "pass": "secret", "user": "omry"}
        }
    finally:
        chdir_hydra_root()


def test_objects_demo(task_runner):  # noqa: F811
    with task_runner(
        calling_file="demos/7_objects/experiment.py",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=[],
    ) as task:
        assert task.job_ret.cfg == {
            "model": {
                "class": "demos.7_objects.objects.Alexnet",
                "params": {"num_layers": 7},
            }
        }
        verify_dir_outputs(task.job_ret, overrides=task.overrides)
