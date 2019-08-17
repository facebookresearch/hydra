# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import subprocess
import sys

import pytest
from omegaconf import OmegaConf

from hydra._internal.core_plugins import BasicLauncher
from hydra.errors import MissingConfigException
from hydra.test_utils.launcher_common_tests import (
    demos_sweep_1_job_test_impl,
    demos_sweep_2_jobs_test_impl,
    demo_6_sweep_test_impl,
    not_sweeping_hydra_overrides,
    sweep_over_two_optimizers,
)
from hydra.test_utils.test_utils import chdir_hydra_root, verify_dir_outputs

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import task_runner, sweep_runner  # noqa: F401

chdir_hydra_root()


def test_missing_conf_dir(task_runner):  # noqa: F811
    with pytest.raises(IOError):
        with task_runner(conf_dir="not_found"):
            pass


def test_missing_conf_file(task_runner):  # noqa: F811
    with pytest.raises(IOError):
        with task_runner(conf_dir=".", conf_filename="not_found"):
            pass


def test_demos_minimal__no_overrides(task_runner):  # noqa: F811
    with task_runner(conf_dir="demos/0_minimal/") as task:
        assert task.job_ret.cfg == {}


def test_demos_minimal__with_overrides(task_runner):  # noqa: F811
    with task_runner(
        conf_dir="demos/0_minimal/", overrides=["abc=123", "a.b=1", "a.a=2"]
    ) as task:
        assert task.job_ret.cfg == dict(abc=123, a=dict(b=1, a=2))
        verify_dir_outputs(task.job_ret.working_dir, task.overrides)


def test_demos_config_file__no_overrides(task_runner):  # noqa: F811
    with task_runner(
        conf_dir="demos/3_config_file/", conf_filename="config.yaml"
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet")
        )

        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_config_file__with_overide(task_runner):  # noqa: F811
    with task_runner(
        conf_dir="demos/3_config_file/",
        conf_filename="config.yaml",
        overrides=["dataset.path=/datasets/imagenet2"],
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet2")
        )
        verify_dir_outputs(task.job_ret.working_dir, task.overrides)


def test_demos_config_splitting(task_runner):  # noqa: F811
    with task_runner(
        conf_dir="demos/4_config_splitting/conf", conf_filename="config.yaml"
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet"),
            optimizer=dict(lr=0.001, type="nesterov"),
        )
        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_config_groups__override_dataset__wrong(task_runner):  # noqa: F811
    with pytest.raises(MissingConfigException) as ex:
        with task_runner(
            conf_dir="demos/5_config_groups/conf", overrides=["optimizer=wrong_name"]
        ):
            pass
    assert sorted(ex.value.options) == sorted(["adam", "nesterov"])


def test_demos_config_groups__override_all_configs(task_runner):  # noqa: F811
    with task_runner(
        conf_dir="demos/5_config_groups/conf",
        overrides=["optimizer=adam", "optimizer.lr=10"],
    ) as task:
        assert task.job_ret.cfg == dict(optimizer=dict(type="adam", lr=10, beta=0.01))
        verify_dir_outputs(task.job_ret.working_dir, overrides=task.overrides)


def test_demos_sweep__override_launcher_basic(task_runner):  # noqa: F811
    with task_runner(
        conf_dir="demos/6_sweep/conf", overrides=["launcher=basic"]
    ) as task:
        assert (
            task.job_ret.hydra_cfg.hydra.launcher["class"]
            == "hydra._internal.core_plugins.basic_launcher.BasicLauncher"
        )
        assert task.job_ret.hydra_cfg.hydra.launcher.params or {} == {}


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
def test_demo_0_minimal(tmpdir, args, output_conf):
    cmd = [sys.executable, "demos/0_minimal/minimal.py", "hydra.run.dir=" + str(tmpdir)]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


def test_demo_1_workdir(tmpdir):
    cmd = [
        sys.executable,
        "demos/1_working_directory/working_directory.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert result.decode("utf-8") == "Working directory : {}\n".format(tmpdir)


@pytest.mark.parametrize(
    "args,expected",
    [
        ([], ["Info level message"]),
        (["-v" "__main__"], ["Info level message", "Debug level message"]),
    ],
)
def test_demo_2_logging(tmpdir, args, expected):
    cmd = [
        sys.executable,
        "demos/2_logging/logging_example.py",
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
                dict(dataset=dict(name="imagenet", path="/datasets/imagenet"))
            ),
        ),
        (
            ["dataset.path=abc"],
            OmegaConf.create(dict(dataset=dict(name="imagenet", path="abc"))),
        ),
    ],
)
def test_demo_3_config_file(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "demos/3_config_file/config_file.py",
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
def test_demo_4_config_slitting(tmpdir, args, output_conf):
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
        ([], OmegaConf.create({"optimizer": {"lr": 0.001, "type": "nesterov"}})),
        (
            ["optimizer=adam"],
            OmegaConf.create({"optimizer": {"beta": 0.01, "lr": 0.1, "type": "adam"}}),
        ),
    ],
)
def test_demo_5_config_groups(tmpdir, args, output_conf):
    cmd = [
        sys.executable,
        "demos/5_config_groups/experiment.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == output_conf


def test_demo_6(tmpdir):
    demo_6_sweep_test_impl(tmpdir, overrides=["launcher=basic"])


def test_fairtask_sweep_1_job(sweep_runner):  # noqa: F811
    demos_sweep_1_job_test_impl(sweep_runner, overrides=["launcher=basic"])


def test_fairtask_sweep_2_jobs(sweep_runner):  # noqa: F811
    demos_sweep_2_jobs_test_impl(sweep_runner, overrides=["launcher=basic"])


def test_not_sweeping_hydra_overrides(sweep_runner):  # noqa: F811
    not_sweeping_hydra_overrides(sweep_runner, overrides=["launcher=basic"])


def test_fairtask_sweep_1_job_strict(sweep_runner):  # noqa: F811
    demos_sweep_1_job_test_impl(sweep_runner, strict=True, overrides=["launcher=basic"])


def test_fairtask_sweep_1_job_strict_and_bad_key(sweep_runner):  # noqa: F811
    with pytest.raises(KeyError):
        demos_sweep_1_job_test_impl(
            sweep_runner, strict=True, overrides=["launcher=basic", "hydra.foo=bar"]
        )


def test_fairtask_sweep_2_optimizers(sweep_runner):  # noqa: F811
    sweep_over_two_optimizers(sweep_runner, overrides=["launcher=basic"])
