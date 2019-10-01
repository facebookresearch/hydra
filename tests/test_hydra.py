# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys

import pytest
import subprocess
from omegaconf import OmegaConf
from hydra import MissingConfigException

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


def test_short_module_name(tmpdir):
    try:
        os.chdir("tutorial/020_config_file")
        cmd = [sys.executable, "my_app.py", "hydra.run.dir=" + str(tmpdir)]
        modified_env = os.environ.copy()
        modified_env["HYDRA_MAIN_MODULE"] = "my_app"
        result = subprocess.check_output(cmd, env=modified_env)
        assert OmegaConf.create(str(result.decode("utf-8"))) == {
            "db": {"driver": "mysql", "pass": "secret", "user": "omry"}
        }
    finally:
        chdir_hydra_root()


@pytest.mark.parametrize(
    "calling_file, calling_module",
    [("tests/test_app/app_with_cfg.py", None), (None, "tests.test_app.app_with_cfg")],
)
@pytest.mark.parametrize("overrides", [["free_group=opt1,opt2"]])
def test_multirun_with_free_override(
    sweep_runner, calling_file, calling_module, overrides  # noqa: F811
):
    sweep = sweep_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="config_with_free_group/config.yaml",
        overrides=overrides,
        strict=True,
    )
    with sweep:
        assert len(sweep.returns[0]) == 2
        assert sweep.returns[0][0].overrides == ["free_group=opt1"]
        assert sweep.returns[0][0].cfg == {"group_opt1": True, "free_group_opt1": True}
        assert sweep.returns[0][1].overrides == ["free_group=opt2"]
        assert sweep.returns[0][1].cfg == {"group_opt1": True, "free_group_opt2": True}
