# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, List

import pytest
from omegaconf import OmegaConf

from hydra import MissingConfigException
from hydra.test_utils.test_utils import (
    TSweepRunner,
    TTaskRunner,
    chdir_hydra_root,
    integration_test,
    verify_dir_outputs,
)

chdir_hydra_root()


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module", [(".", None), (None, ".")]
)
def test_missing_conf_dir(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with pytest.raises(MissingConfigException):
        with task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="dir_not_found",
            config_name=None,
        ):
            pass


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_without_config/my_app.py", None),
        (None, "tests.test_apps.app_without_config.my_app"),
    ],
)
def test_missing_conf_file(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with pytest.raises(MissingConfigException):
        with task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="not_found.yaml",
            config_name=None,
        ):
            pass


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_without_config/my_app.py", None),
        (None, "tests.test_apps.app_without_config.my_app"),
    ],
)
def test_app_without_config___no_overrides(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name=None,
    ) as task:
        assert task.job_ret is not None
        assert task.job_ret.cfg == {}


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/hydra_main_rerun/my_app.py", None),
        (None, "tests.test_apps.hydra_main_rerun.my_app"),
    ],
)
def test_hydra_main_rerun(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name=None,
    ) as task:
        assert task.job_ret is not None
        assert task.job_ret.cfg == {}


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_without_config/my_app.py", None),
        (None, "tests.test_apps.app_without_config.my_app"),
    ],
)
def test_app_without_config__with_overrides(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="",
        config_name=None,
        overrides=["abc=123", "a.b=1", "a.a=2"],
    ) as task:
        assert task.job_ret is not None and task.job_ret.cfg == dict(
            abc=123, a=dict(b=1, a=2)
        )
        verify_dir_outputs(task.job_ret, task.overrides)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg.my_app"),
    ],
)
def test_app_with_config_file__no_overrides(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:

    task = task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,  # Testing legacy mode, both path and named are in config_path
        config_name="config.yaml",
    )
    with task:
        assert task.job_ret is not None and task.job_ret.cfg == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }

        verify_dir_outputs(task.job_ret)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg_groups/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg_groups.my_app"),
    ],
)
def test_app_with_config_path_backward_compatibility(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    task = task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="conf/config.yaml",  # Testing legacy mode, both path and named are in config_path
        config_name=None,
    )
    with task:

        assert task.job_ret is not None and task.job_ret.cfg == {
            "optimizer": {"type": "nesterov", "lr": 0.001}
        }

        verify_dir_outputs(task.job_ret)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg.my_app"),
    ],
)
def test_app_with_config_file__with_overide(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name="config.yaml",
        overrides=["dataset.path=/datasets/imagenet2"],
    ) as task:
        assert task.job_ret is not None and task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet2")
        )
        verify_dir_outputs(task.job_ret, task.overrides)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_split_cfg/my_app.py", None),
        (None, "tests.test_apps.app_with_split_cfg.my_app"),
    ],
)
def test_app_with_split_config(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name="config.yaml",
    ) as task:
        assert task.job_ret is not None and task.job_ret.cfg == dict(
            dataset=dict(name="imagenet", path="/datasets/imagenet"),
            optimizer=dict(lr=0.001, type="nesterov"),
        )
        verify_dir_outputs(task.job_ret)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg_groups/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg_groups.my_app"),
    ],
)
def test_app_with_config_groups__override_dataset__wrong(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with pytest.raises(MissingConfigException) as ex:
        with task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="conf",
            config_name=None,
            overrides=["optimizer=wrong_name"],
        ):
            pass
    assert sorted(ex.value.options) == sorted(["adam", "nesterov"])


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg_groups/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg_groups.my_app"),
    ],
)
def test_app_with_config_groups__override_all_configs(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="conf",
        config_name=None,
        overrides=["optimizer=adam", "optimizer.lr=10"],
    ) as task:
        assert task.job_ret is not None and task.job_ret.cfg == dict(
            optimizer=dict(type="adam", lr=10, beta=0.01)
        )
        verify_dir_outputs(task.job_ret, overrides=task.overrides)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_custom_launcher/my_app.py", None),
        (None, "tests.test_apps.app_with_custom_launcher.my_app"),
    ],
)
def test_app_with_sweep_cfg__override_to_basic_launcher(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name="config.yaml",
        overrides=["hydra/launcher=basic"],
    ) as task:
        assert task.job_ret is not None
        assert task.job_ret.hydra_cfg is not None
        hydra_cfg = task.job_ret.hydra_cfg
        assert (
            hydra_cfg.hydra.launcher.cls
            == "hydra._internal.core_plugins.basic_launcher.BasicLauncher"
        )
        assert len(task.job_ret.hydra_cfg.hydra.launcher.params) == 0


def test_short_module_name(tmpdir: Path) -> None:
    try:
        os.chdir("examples/tutorial/2_config_file")
        cmd = [sys.executable, "my_app.py", "hydra.run.dir=" + str(tmpdir)]
        result = subprocess.check_output(cmd)
        assert OmegaConf.create(str(result.decode("utf-8"))) == {
            "db": {"driver": "mysql", "pass": "secret", "user": "omry"}
        }
    finally:
        chdir_hydra_root()


def test_hydra_main_module_override_name(tmpdir: Path) -> None:
    cfg = OmegaConf.create()
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=[],
        prints="HydraConfig.get().job.name",
        expected_outputs="Foo",
        env_override={"HYDRA_MAIN_MODULE": "hydra.test_utils.configs.Foo"},
    )


def test_short_hydra_main_module_override_name(tmpdir: Path) -> None:
    cfg = OmegaConf.create()
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=[],
        prints="HydraConfig.get().job.name",
        expected_outputs="Foo",
        env_override={"HYDRA_MAIN_MODULE": "Foo"},
    )


@pytest.mark.parametrize(  # type: ignore
    "env_name", ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE", "FB_XAR_MAIN_MODULE"]
)
def test_module_env_override(tmpdir: Path, env_name: str) -> None:
    """
    Tests that module name overrides are working.
    """
    try:
        os.chdir("examples/tutorial/2_config_file")
        cmd = [sys.executable, "my_app.py", "hydra.run.dir=" + str(tmpdir)]
        modified_env = os.environ.copy()
        modified_env[env_name] = "hydra.test_utils.configs.Foo"
        result = subprocess.check_output(cmd, env=modified_env)
        assert OmegaConf.create(str(result.decode("utf-8"))) == {
            "normal_yaml_config": True
        }
    finally:
        chdir_hydra_root()


@pytest.mark.parametrize(  # type: ignore
    "flag,expected_keys",
    [("--cfg=all", ["db", "hydra"]), ("--cfg=hydra", ["hydra"]), ("--cfg=job", ["db"])],
)
def test_cfg(tmpdir: Path, flag: str, expected_keys: List[str]) -> None:
    try:
        os.chdir("examples/tutorial/4_defaults")
        cmd = [sys.executable, "my_app.py", "hydra.run.dir=" + str(tmpdir), flag]
        result = subprocess.check_output(cmd)
        conf = OmegaConf.create(str(result.decode("utf-8")))
        for key in expected_keys:
            assert key in conf
    finally:
        chdir_hydra_root()


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_config_with_free_group/my_app.py", None),
        (None, "tests.test_apps.app_with_config_with_free_group.my_app"),
    ],
)
@pytest.mark.parametrize("overrides", [["free_group=opt1,opt2"]])  # type: ignore
def test_multirun_with_free_override(
    restore_singletons: Any,
    sweep_runner: TSweepRunner,
    calling_file: str,
    calling_module: str,
    overrides: List[str],
) -> None:
    sweep = sweep_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="conf/",
        config_name="config.yaml",
        task_function=None,
        overrides=overrides,
        strict=True,
    )
    with sweep:
        assert sweep.returns is not None and len(sweep.returns[0]) == 2
        assert sweep.returns[0][0].overrides == ["free_group=opt1"]
        assert sweep.returns[0][0].cfg == {"group_opt1": True, "free_group_opt1": True}
        assert sweep.returns[0][1].overrides == ["free_group=opt2"]
        assert sweep.returns[0][1].cfg == {"group_opt1": True, "free_group_opt2": True}


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        pytest.param(
            "tests/test_apps/sweep_complex_defaults/my_app.py", None, id="file_path"
        ),
        pytest.param(
            None, "tests.test_apps.sweep_complex_defaults.my_app", id="pkg_path"
        ),
    ],
)
def test_sweep_complex_defaults(
    restore_singletons: Any,
    sweep_runner: TSweepRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with sweep_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="conf",
        config_name="config.yaml",
        task_function=None,
        overrides=["optimizer=adam,nesterov"],
    ) as sweep:
        assert sweep.returns is not None and len(sweep.returns[0]) == 2
        assert sweep.returns[0][0].overrides == ["optimizer=adam"]
        assert sweep.returns[0][1].overrides == ["optimizer=nesterov"]


@pytest.mark.parametrize(  # type: ignore
    "script, flag, overrides,expected",
    [
        (
            "examples/tutorial/1_simple_cli_app/my_app.py",
            "--help",
            ["hydra.help.template=foo"],
            "foo\n",
        ),
        (
            "examples/tutorial/1_simple_cli_app/my_app.py",
            "--help",
            ["hydra.help.template=$CONFIG", "foo=bar"],
            """foo: bar

""",
        ),
        (
            "examples/tutorial/1_simple_cli_app/my_app.py",
            "--help",
            ["hydra.help.template=$FLAGS_HELP"],
            """--help,-h : Application's help
--hydra-help : Hydra's help
--version : show program's version number and exit
--cfg,-c : Show config instead of running [job|hydra|all]
--run,-r : Run a job
--multirun,-m : Run multiple jobs with the configured launcher
--shell_completion,-sc : Install or Uninstall shell completion:
    Install:
    eval "$(python examples/tutorial/1_simple_cli_app/my_app.py -sc install=SHELL_NAME)"

    Uninstall:
    eval "$(python examples/tutorial/1_simple_cli_app/my_app.py -sc uninstall=SHELL_NAME)"

Overrides : Any key=value arguments to override config values (use dots for.nested=overrides)
""",
        ),
        (
            "examples/tutorial/3_config_groups/my_app.py",
            "--help",
            ["hydra.help.template=$APP_CONFIG_GROUPS"],
            """db: mysql, postgresql

""",
        ),
        (
            "examples/tutorial/1_simple_cli_app/my_app.py",
            "--hydra-help",
            ["hydra.hydra_help.template=foo"],
            "foo\n",
        ),
        (
            "examples/tutorial/1_simple_cli_app/my_app.py",
            "--hydra-help",
            ["hydra.hydra_help.template=$FLAGS_HELP"],
            """--help,-h : Application's help
--hydra-help : Hydra's help
--version : show program's version number and exit
--cfg,-c : Show config instead of running [job|hydra|all]
--run,-r : Run a job
--multirun,-m : Run multiple jobs with the configured launcher
--shell_completion,-sc : Install or Uninstall shell completion:
    Install:
    eval "$(python examples/tutorial/1_simple_cli_app/my_app.py -sc install=SHELL_NAME)"

    Uninstall:
    eval "$(python examples/tutorial/1_simple_cli_app/my_app.py -sc uninstall=SHELL_NAME)"

Overrides : Any key=value arguments to override config values (use dots for.nested=overrides)
""",
        ),
    ],
)
def test_help(
    tmpdir: Path, script: str, flag: str, overrides: List[str], expected: Any
) -> None:
    cmd = [sys.executable, script, "hydra.run.dir=" + str(tmpdir)]
    cmd.extend(overrides)
    cmd.append(flag)
    print(" ".join(cmd))
    result = str(subprocess.check_output(cmd).decode("utf-8"))
    # normalize newlines on Windows to make testing easier
    result = result.replace("\r\n", "\n")
    assert result == expected


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/interpolating_dir_hydra_to_app/my_app.py", None),
        (None, "tests.test_apps.interpolating_dir_hydra_to_app.my_app"),
    ],
)
def test_interpolating_dir_hydra_to_app(
    restore_singletons: Any,
    task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    basedir = "foo"
    with task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name="config.yaml",
        overrides=["experiment.base_dir=" + basedir],
    ) as task:
        assert task.temp_dir is not None
        path = Path(task.temp_dir) / basedir
        assert path.exists()


def test_sys_exit(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "tests/test_apps/sys_exit/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    assert subprocess.run(cmd).returncode == 42
