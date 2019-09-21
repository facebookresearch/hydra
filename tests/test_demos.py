# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import os
import subprocess
import sys

import pytest
from omegaconf import OmegaConf

from hydra.errors import MissingConfigException
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


@pytest.mark.parametrize("calling_file, calling_module", [(".", None), (None, ".")])
def test_missing_conf_dir(task_runner, calling_file, calling_module):  # noqa: F811
    with pytest.raises(MissingConfigException):
        with task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="dir_not_found",
        ):
            pass


@pytest.mark.parametrize(
    "calling_file, calling_module", [("hydra/app.py", None), (None, "hydra.app")]
)
def test_missing_conf_file(task_runner, calling_file, calling_module):  # noqa: F811
    with pytest.raises(MissingConfigException):
        with task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="not_found.yaml",
        ):
            pass


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app.py", None), (None, "tests.test_app.app")],
)
def test_app_without_config___no_overrides(
    task_runner, calling_file, calling_module  # noqa: F811
):
    with task_runner(
        calling_file=calling_file, calling_module=calling_module, config_path=""
    ) as task:
        assert task.job_ret.cfg == {}


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app.py", None), (None, "tests.test_app.app")],
)
def test_app_without_config__with_overrides(
    task_runner, calling_file, calling_module  # noqa: F811
):
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="",
        overrides=["abc=123", "a.b=1", "a.a=2"],
    ) as task:
        assert task.job_ret.cfg == dict(abc=123, a=dict(b=1, a=2))
        verify_dir_outputs(task.job_ret, task.overrides)


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app_with_cfg.py", None), (None, "tests.test_app.app_with_cfg")],
)
def test_app_with_config_file__no_overrides(
    task_runner, calling_file, calling_module  # noqa: F811
):
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="config.yaml",
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet")
        )

        verify_dir_outputs(task.job_ret)


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app_with_cfg.py", None), (None, "tests.test_app.app_with_cfg")],
)
def test_app_with_config_file__with_overide(
    task_runner, calling_file, calling_module  # noqa: F811
):
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="config.yaml",
        overrides=["dataset.path=/datasets/imagenet2"],
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet2")
        )
        verify_dir_outputs(task.job_ret, task.overrides)


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app_with_cfg.py", None), (None, "tests.test_app.app_with_cfg")],
)
def test_app_with_split_config(task_runner, calling_file, calling_module):  # noqa: F811
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="split_cfg/config.yaml",
    ) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet"),
            optimizer=dict(lr=0.001, type="nesterov"),
        )
        verify_dir_outputs(task.job_ret)


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app_with_cfg.py", None), (None, "tests.test_app.app_with_cfg")],
)
def test_app_with_config_groups__override_dataset__wrong(
    task_runner, calling_file, calling_module  # noqa: F811
):
    with pytest.raises(MissingConfigException) as ex:
        with task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="cfg_groups",
            overrides=["optimizer=wrong_name"],
        ):
            pass
    assert sorted(ex.value.options) == sorted(["adam", "nesterov"])


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app_with_cfg.py", None), (None, "tests.test_app.app_with_cfg")],
)
def test_app_with_config_groups__override_all_configs(
    task_runner, calling_file, calling_module  # noqa: F811
):
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="cfg_groups",
        overrides=["optimizer=adam", "optimizer.lr=10"],
    ) as task:
        assert task.job_ret.cfg == dict(optimizer=dict(type="adam", lr=10, beta=0.01))
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app_with_cfg.py", None), (None, "tests.test_app.app_with_cfg")],
)
def test_app_with_sweep_cfg__override_to_basic_launcher(
    task_runner, calling_file, calling_module  # noqa: F811
):
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="sweep_cfg/config.yaml",
        overrides=["hydra/launcher=basic"],
    ) as task:
        hydra_cfg = task.job_ret.hydra_cfg
        assert (
            hydra_cfg.hydra.launcher["class"]
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
    assert result.decode("utf-8").rstrip() == "Working directory : {}".format(tmpdir)


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


def test_short_module_name():
    try:
        os.chdir("demos/3_config_file")
        cmd = [sys.executable, "config_file.py"]
        modified_env = os.environ.copy()
        modified_env["HYDRA_MAIN_MODULE"] = "config_file"
        result = subprocess.check_output(cmd, env=modified_env)
        assert OmegaConf.create(str(result.decode("utf-8"))) == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet")
        )
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
