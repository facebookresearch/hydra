# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import re
import subprocess
import sys
from logging import getLogger
from pathlib import Path
from textwrap import dedent
from typing import Any, List, Optional, Set

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra import MissingConfigException
from hydra.test_utils.test_utils import (
    TSweepRunner,
    TTaskRunner,
    assert_text_same,
    chdir_hydra_root,
    get_run_output,
    integration_test,
    normalize_newlines,
    run_with_error,
    verify_dir_outputs,
)

chdir_hydra_root()


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module", [(".", None), (None, ".")]
)
def test_missing_conf_dir(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with pytest.raises(MissingConfigException):
        with hydra_task_runner(
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with pytest.raises(MissingConfigException):
        with hydra_task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path=None,
            config_name="not_found.yaml",
        ):
            pass


def test_run_dir() -> None:
    get_run_output(["tests/test_apps/run_dir_test/my_app.py"])


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_without_config/my_app.py", None),
        (None, "tests.test_apps.app_without_config.my_app"),
    ],
)
def test_app_without_config___no_overrides(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_task_runner(
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_task_runner(
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
def test_app_without_config__with_append(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="",
        config_name=None,
        overrides=["+abc=123", "+a.b=1", "+a.a=2"],
        configure_logging=True,
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    task = hydra_task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,  # Testing legacy mode, both path and named are in config_path
        config_name="config.yaml",
        configure_logging=True,
    )
    with task:
        assert task.job_ret is not None and task.job_ret.cfg == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }

        verify_dir_outputs(task.job_ret)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg_groups_no_header/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg_groups_no_header.my_app"),
    ],
)
def test_config_without_package_header_warnings(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
    recwarn: Any,
) -> None:
    task = hydra_task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="conf",
        config_name="config.yaml",
    )
    with task:
        assert task.job_ret is not None and task.job_ret.cfg == {
            "optimizer": {"type": "nesterov", "lr": 0.001}
        }

    assert len(recwarn) == 1
    msg = recwarn.pop().message.args[0]
    assert "Missing @package directive optimizer/nesterov.yaml in " in msg
    assert (
        "See https://hydra.cc/docs/next/upgrades/0.11_to_1.0/adding_a_package_directive"
        in msg
    )


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg_groups/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg_groups.my_app"),
    ],
)
def test_app_with_config_path_backward_compatibility(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    msg = (
        "\nUsing config_path to specify the config name is deprecated, specify the config name via config_name"
        "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/config_path_changes"
    )

    with pytest.warns(expected_warning=UserWarning, match=re.escape(msg)):
        task = hydra_task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="conf/config.yaml",  # Testing legacy mode, both path and named are in config_path
            config_name=None,
            configure_logging=True,
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name="config.yaml",
        overrides=["dataset.path=/datasets/imagenet2"],
        configure_logging=True,
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name="config.yaml",
        configure_logging=True,
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with pytest.raises(MissingConfigException) as ex:
        with hydra_task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="conf",
            config_name=None,
            overrides=["+optimizer=wrong_name"],
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="conf",
        config_name=None,
        overrides=["+optimizer=adam", "optimizer.lr=10"],
        configure_logging=True,
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
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_task_runner(
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
            hydra_cfg.hydra.launcher._target_
            == "hydra._internal.core_plugins.basic_launcher.BasicLauncher"
        )
        assert len(task.job_ret.hydra_cfg.hydra.launcher) == 1


def test_short_module_name(tmpdir: Path) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    out, _err = get_run_output(cmd)
    assert OmegaConf.create(out) == {
        "db": {"driver": "mysql", "password": "secret", "user": "omry"}
    }


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


@pytest.mark.parametrize(  # type: ignore
    "env_name", ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE", "FB_XAR_MAIN_MODULE"]
)
def test_module_env_override(tmpdir: Path, env_name: str) -> None:
    """
    Tests that module name overrides are working.
    """
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    modified_env = os.environ.copy()
    modified_env[env_name] = "hydra.test_utils.configs.Foo"
    result, _err = get_run_output(cmd, env=modified_env)
    assert OmegaConf.create(result) == {"normal_yaml_config": True}


@pytest.mark.parametrize(  # type: ignore
    "flag,expected_keys",
    [("--cfg=all", ["db", "hydra"]), ("--cfg=hydra", ["hydra"]), ("--cfg=job", ["db"])],
)
def test_cfg(tmpdir: Path, flag: str, expected_keys: List[str]) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/5_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        flag,
    ]
    result, _err = get_run_output(cmd)
    conf = OmegaConf.create(result)
    for key in expected_keys:
        assert key in conf


@pytest.mark.parametrize(  # type: ignore
    "flags,expected",
    [
        pytest.param(
            ["--cfg=job"],
            """# @package _global_
db:
  driver: mysql
  user: omry
  pass: secret
""",
            id="no-package",
        ),
        pytest.param(
            ["--cfg=job", "--package=_global_"],
            """# @package _global_
db:
  driver: mysql
  user: omry
  pass: secret
""",
            id="package=_global_",
        ),
        pytest.param(
            ["--cfg=job", "--package=db"],
            """# @package db
driver: mysql
user: omry
pass: secret
""",
            id="package=db",
        ),
        pytest.param(
            ["--cfg=job", "--package=db.driver"], "mysql\n", id="package=db.driver"
        ),
    ],
)
def test_cfg_with_package(tmpdir: Path, flags: List[str], expected: str) -> None:
    cmd = [
        "examples/tutorials/basic/your_first_hydra_app/5_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ] + flags

    result, _err = get_run_output(cmd)
    assert normalize_newlines(result) == expected.rstrip()


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_config_with_free_group/my_app.py", None),
        (None, "tests.test_apps.app_with_config_with_free_group.my_app"),
    ],
)
@pytest.mark.parametrize("overrides", [["+free_group=opt1,opt2"]])  # type: ignore
def test_multirun_with_free_override(
    hydra_restore_singletons: Any,
    hydra_sweep_runner: TSweepRunner,
    calling_file: str,
    calling_module: str,
    overrides: List[str],
) -> None:
    sweep = hydra_sweep_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path="conf/",
        config_name="config.yaml",
        task_function=None,
        overrides=overrides,
    )
    with sweep:
        assert sweep.returns is not None and len(sweep.returns[0]) == 2
        assert sweep.returns[0][0].overrides == ["+free_group=opt1"]
        assert sweep.returns[0][0].cfg == {"group_opt1": True, "free_group_opt1": True}
        assert sweep.returns[0][1].overrides == ["+free_group=opt2"]
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
    hydra_restore_singletons: Any,
    hydra_sweep_runner: TSweepRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    with hydra_sweep_runner(
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
        pytest.param(
            "examples/tutorials/basic/your_first_hydra_app/1_simple_cli/my_app.py",
            "--help",
            ["hydra.help.template=foo"],
            "foo\n",
            id="simple_cli_app",
        ),
        pytest.param(
            "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
            "--help",
            ["hydra.help.template=foo"],
            "foo\n",
            id="overriding_help_template",
        ),
        pytest.param(
            "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
            "--help",
            ["hydra.help.template=$CONFIG", "db.user=root"],
            """db:
  driver: mysql
  user: root
  password: secret

""",
            id="overriding_help_template:$CONFIG",
        ),
        pytest.param(
            "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
            "--help",
            ["hydra.help.template=$FLAGS_HELP"],
            """--help,-h : Application's help
--hydra-help : Hydra's help
--version : Show Hydra's version and exit
--cfg,-c : Show config instead of running [job|hydra|all]
--package,-p : Config package to show
--run,-r : Run a job
--multirun,-m : Run multiple jobs with the configured launcher and sweeper
--shell-completion,-sc : Install or Uninstall shell completion:
    Bash - Install:
    eval "$(python {script} -sc install=bash)"
    Bash - Uninstall:
    eval "$(python {script} -sc uninstall=bash)"

    Fish - Install:
    python {script} -sc install=fish | source
    Fish - Uninstall:
    python {script} -sc uninstall=fish | source

--config-path,-cp : Overrides the config_path specified in hydra.main().
                    The config_path is relative to the Python file declaring @hydra.main()
--config-name,-cn : Overrides the config_name specified in hydra.main()
--config-dir,-cd : Adds an additional config dir to the config search path
--info,-i : Print Hydra information
Overrides : Any key=value arguments to override config values (use dots for.nested=overrides)
""",
            id="overriding_help_template:$FLAGS_HELP",
        ),
        pytest.param(
            "examples/tutorials/basic/your_first_hydra_app/4_config_groups/my_app.py",
            "--help",
            ["hydra.help.template=$APP_CONFIG_GROUPS"],
            """db: mysql, postgresql

""",
            id="overriding_help_template:$APP_CONFIG_GROUPS",
        ),
        pytest.param(
            "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
            "--hydra-help",
            ["hydra.hydra_help.template=foo"],
            "foo\n",
            id="overriding_hydra_help_template",
        ),
        pytest.param(
            "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
            "--hydra-help",
            ["hydra.hydra_help.template=$FLAGS_HELP"],
            """--help,-h : Application's help
--hydra-help : Hydra's help
--version : Show Hydra's version and exit
--cfg,-c : Show config instead of running [job|hydra|all]
--package,-p : Config package to show
--run,-r : Run a job
--multirun,-m : Run multiple jobs with the configured launcher and sweeper
--shell-completion,-sc : Install or Uninstall shell completion:
    Bash - Install:
    eval "$(python {script} -sc install=bash)"
    Bash - Uninstall:
    eval "$(python {script} -sc uninstall=bash)"

    Fish - Install:
    python {script} -sc install=fish | source
    Fish - Uninstall:
    python {script} -sc uninstall=fish | source

--config-path,-cp : Overrides the config_path specified in hydra.main().
                    The config_path is relative to the Python file declaring @hydra.main()
--config-name,-cn : Overrides the config_name specified in hydra.main()
--config-dir,-cd : Adds an additional config dir to the config search path
--info,-i : Print Hydra information
Overrides : Any key=value arguments to override config values (use dots for.nested=overrides)
""",
            id="overriding_hydra_help_template:$FLAGS_HELP",
        ),
    ],
)
def test_help(
    tmpdir: Path, script: str, flag: str, overrides: List[str], expected: Any
) -> None:
    cmd = [script, "hydra.run.dir=" + str(tmpdir)]
    cmd.extend(overrides)
    cmd.append(flag)
    result, _err = get_run_output(cmd)
    # normalize newlines on Windows to make testing easier
    assert result == normalize_newlines(expected.format(script=script)).rstrip()


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/interpolating_dir_hydra_to_app/my_app.py", None),
        (None, "tests.test_apps.interpolating_dir_hydra_to_app.my_app"),
    ],
)
def test_interpolating_dir_hydra_to_app(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
) -> None:
    basedir = "foo"
    with hydra_task_runner(
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
        "-Werror",
        "tests/test_apps/sys_exit/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    assert subprocess.run(cmd).returncode == 42


@pytest.mark.parametrize(  # type: ignore
    "task_config, overrides, expected_dir",
    [
        ({"hydra": {"run": {"dir": "foo"}}}, [], "foo"),
        ({}, ["hydra.run.dir=bar"], "bar"),
        ({"hydra": {"run": {"dir": "foo"}}}, ["hydra.run.dir=boom"], "boom"),
        (
            {
                "hydra": {"run": {"dir": "foo-${hydra.job.override_dirname}"}},
                "app": {"a": 1, "b": 2},
            },
            ["app.a=20"],
            "foo-app.a=20",
        ),
        (
            {
                "hydra": {"run": {"dir": "foo-${hydra.job.override_dirname}"}},
                "app": {"a": 1, "b": 2},
            },
            ["app.b=10", "app.a=20"],
            "foo-app.a=20,app.b=10",
        ),
    ],
)
def test_local_run_workdir(
    tmpdir: Path, task_config: DictConfig, overrides: List[str], expected_dir: str
) -> None:
    cfg = OmegaConf.create(task_config)
    assert isinstance(cfg, DictConfig)
    expected_dir1 = tmpdir / expected_dir
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=overrides,
        prints="os.getcwd()",
        expected_outputs=str(expected_dir1),
    )


def test_hydra_env_set_with_config(tmpdir: Path) -> None:
    cfg = OmegaConf.create({"hydra": {"job": {"env_set": {"foo": "bar"}}}})
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=[],
        prints="os.environ['foo']",
        expected_outputs="bar",
    )


def test_hydra_env_set_with_override(tmpdir: Path) -> None:
    integration_test(
        tmpdir=tmpdir,
        task_config={},
        overrides=["+hydra.job.env_set.foo=bar"],
        prints="os.environ['foo']",
        expected_outputs="bar",
    )


@pytest.mark.parametrize(  # type: ignore
    "override", [pytest.param("xyz", id="db=xyz"), pytest.param("", id="db=")]
)
@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        pytest.param("hydra/test_utils/example_app.py", None, id="file"),
        pytest.param(None, "hydra.test_utils.example_app", id="module"),
    ],
)
def test_override_with_invalid_group_choice(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
    override: str,
) -> None:
    msg = (
        f"Could not load db/{override}."
        f"\nAvailable options:"
        f"\n\tmysql"
        f"\n\tpostgresql"
    )

    with pytest.raises(MissingConfigException, match=re.escape(msg)):
        with hydra_task_runner(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path="configs",
            config_name="db_conf",
            overrides=[f"db={override}"],
        ):
            ...


@pytest.mark.parametrize("config_path", ["dir1", "dir2"])  # type: ignore
@pytest.mark.parametrize("config_name", ["cfg1", "cfg2"])  # type: ignore
def test_config_name_and_path_overrides(
    tmpdir: Path, config_path: str, config_name: str
) -> None:
    cmd = [
        "tests/test_apps/app_with_multiple_config_dirs/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        f"--config-name={config_name}",
        f"--config-path={config_path}",
    ]
    print(" ".join(cmd))
    result, _err = get_run_output(cmd)
    # normalize newlines on Windows to make testing easier
    result = result.replace("\r\n", "\n")
    assert result == f"{config_path}_{config_name}: true"


@pytest.mark.parametrize(  # type: ignore
    "overrides, expected_files",
    [
        ([], {".hydra"}),
        (["hydra.output_subdir=foo"], {"foo"}),
        (["hydra.output_subdir=null"], set()),
    ],
)
@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg/my_app.py", None),
        (None, "tests.test_apps.app_with_cfg.my_app"),
    ],
)
def test_hydra_output_dir(
    hydra_restore_singletons: Any,
    hydra_task_runner: TTaskRunner,
    calling_file: str,
    calling_module: str,
    overrides: List[str],
    expected_files: Set[str],
) -> None:
    with hydra_task_runner(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=None,
        config_name=None,
        overrides=overrides,
    ) as task:
        assert task.temp_dir is not None
        path = Path(task.temp_dir)
        files = set([str(x)[len(task.temp_dir) + 1 :] for x in path.iterdir()])
        assert files == expected_files


@pytest.mark.parametrize(  # type: ignore
    "directory,file,module, error",
    [
        (
            "tests/test_apps/run_as_module/1",
            "my_app.py",
            "my_app",
            "Primary config module is empty",
        ),
        ("tests/test_apps/run_as_module/2", "my_app.py", "my_app", None),
        ("tests/test_apps/run_as_module/3", "module/my_app.py", "module.my_app", None),
        ("tests/test_apps/run_as_module/4", "module/my_app.py", "module.my_app", None),
    ],
)
def test_module_run(
    tmpdir: Any, directory: str, file: str, module: str, error: Optional[str]
) -> None:
    cmd = [
        directory + "/" + file,
        "hydra.run.dir=" + str(tmpdir),
    ]
    modified_env = os.environ.copy()
    modified_env["PYTHONPATH"] = directory
    modified_env["HYDRA_MAIN_MODULE"] = module
    if error is not None:
        ret = run_with_error(cmd, modified_env)
        assert re.search(re.escape(error), ret) is not None
    else:
        result, _err = get_run_output(cmd, env=modified_env)
        assert OmegaConf.create(result) == {"x": 10}


@pytest.mark.parametrize(  # type: ignore
    "overrides,error,expected",
    [
        pytest.param(["test.param=1"], False, "1", id="run:value"),
        pytest.param(
            ["test.param=1,2"],
            True,
            dedent(
                """\
            Ambiguous value for argument 'test.param=1,2'
            1. To use it as a list, use key=[value1,value2]
            2. To use it as string, quote the value: key=\\'value1,value2\\'
            3. To sweep over it, add --multirun to your command line

            Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace."""
            ),
            id="run:choice_sweep",
        ),
        pytest.param(
            ["test.param=[1,2]"],
            True,
            dedent(
                """\
                Error merging override test.param=[1,2]
                Value '[1, 2]' could not be converted to Integer
                \tfull_key: test.param
                \treference_type=Optional[TestConfig]
                \tobject_type=TestConfig

                Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace."""
            ),
            id="run:list_value",
        ),
        pytest.param(["test.param=1", "-m"], False, "1", id="multirun:value"),
        pytest.param(
            ["test.param=1,2", "-m"], False, "1\n2", id="multirun:choice_sweep"
        ),
    ],
)
def test_multirun_structured_conflict(
    tmpdir: Any, overrides: List[str], error: bool, expected: Any
) -> None:
    cmd = [
        "tests/test_apps/multirun_structured_conflict/my_app.py",
        "hydra.sweep.dir=" + str(tmpdir),
    ]
    cmd.extend(overrides)
    if error:
        expected = normalize_newlines(expected)
        ret = normalize_newlines(run_with_error(cmd))
        assert re.search(re.escape(expected), ret) is not None
    else:
        ret, _err = get_run_output(cmd)
        assert ret == expected


@pytest.mark.parametrize(
    "cmd_base",
    [(["tests/test_apps/simple_app/my_app.py", "hydra/hydra_logging=disabled"])],
)
class TestVariousRuns:
    @pytest.mark.parametrize(  # type: ignore
        "sweep", [pytest.param(False, id="run"), pytest.param(True, id="sweep")]
    )
    def test_run_with_missing_default(
        self, cmd_base: List[str], tmpdir: Any, sweep: bool
    ) -> None:
        cmd = cmd_base + [
            "hydra.sweep.dir=" + str(tmpdir),
            "--config-name=unspecified_mandatory_default",
            "--config-path=../../../hydra/test_utils/configs",
        ]
        if sweep:
            cmd.append("-m")
        expected = """You must specify 'group1', e.g, group1=<OPTION>
Available options:
\tabc.cde
\tfile1
\tfile2"""
        ret = run_with_error(cmd)
        assert re.search(re.escape(expected), ret) is not None

    def test_command_line_interpolations_evaluated_lazily(
        self, cmd_base: List[str], tmpdir: Any
    ) -> None:
        cmd = cmd_base + [
            "hydra.sweep.dir=" + str(tmpdir),
            "+foo=10,20",
            "+bar=${foo}",
            "--multirun",
        ]
        expected = """foo: 10
bar: 10

foo: 20
bar: 20"""
        ret, _err = get_run_output(cmd)
        assert normalize_newlines(ret) == normalize_newlines(expected)

    def test_multirun_config_overrides_evaluated_lazily(
        self, cmd_base: List[str], tmpdir: Any
    ) -> None:
        cmd = cmd_base + [
            "hydra.sweep.dir=" + str(tmpdir),
            "+foo=10,20",
            "+bar=${foo}",
            "--multirun",
        ]
        expected = """foo: 10
bar: 10

foo: 20
bar: 20"""
        ret, _err = get_run_output(cmd)
        assert normalize_newlines(ret) == normalize_newlines(expected)

    def test_multirun_defaults_override(self, cmd_base: List[str], tmpdir: Any) -> None:
        cmd = cmd_base + [
            "hydra.sweep.dir=" + str(tmpdir),
            "group1=file1,file2",
            "--multirun",
            "--config-path=../../../hydra/test_utils/configs",
            "--config-name=compose",
        ]
        expected = """foo: 10
bar: 100

foo: 20
bar: 100"""
        ret, _err = get_run_output(cmd)
        assert normalize_newlines(ret) == normalize_newlines(expected)

    def test_run_pass_list(self, cmd_base: List[str], tmpdir: Any) -> None:
        cmd = cmd_base + [
            "hydra.sweep.dir=" + str(tmpdir),
            "+foo=[1,2,3]",
        ]
        expected = {"foo": [1, 2, 3]}
        ret, _err = get_run_output(cmd)
        assert OmegaConf.create(ret) == OmegaConf.create(expected)


def test_app_with_error_exception_sanitized(tmpdir: Any, monkeypatch: Any) -> None:
    monkeypatch.chdir("tests/test_apps/app_with_runtime_config_error")
    cmd = [
        "my_app.py",
        "hydra.sweep.dir=" + str(tmpdir),
    ]
    expected = """Traceback (most recent call last):
  File "my_app.py", line 13, in my_app
    foo(cfg)
  File "my_app.py", line 8, in foo
    cfg.foo = "bar"  # does not exist in the config
omegaconf.errors.ConfigAttributeError: Key 'foo' is not in struct
\tfull_key: foo
\treference_type=Optional[Dict[Union[str, Enum], Any]]
\tobject_type=dict

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace."""

    ret = run_with_error(cmd)
    assert normalize_newlines(expected) == normalize_newlines(ret)


def test_hydra_to_job_config_interpolation(tmpdir: Any) -> Any:
    cmd = [
        "tests/test_apps/hydra_to_cfg_interpolation/my_app.py",
        "hydra.sweep.dir=" + str(tmpdir),
        "b=${a}",
        "a=foo",
    ]
    expected = "override_a=foo,b=foo"
    result, _err = get_run_output(cmd)
    assert result == expected.strip()


@pytest.mark.parametrize(  # type: ignore
    "overrides,expected",
    [
        pytest.param(
            ["dataset=imagenet"], {"dataset": {"name": "imagenet"}}, id="no_conf_dir"
        ),
        pytest.param(
            ["dataset=cifar10", "--config-dir=user-dir"],
            {"dataset": {"name": "cifar10"}},
            id="no_conf_dir",
        ),
    ],
)
def test_config_dir_argument(
    monkeypatch: Any, tmpdir: Path, overrides: List[str], expected: DictConfig
) -> None:
    monkeypatch.chdir("tests/test_apps/user-config-dir")
    cmd = [
        "my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    cmd.extend(overrides)
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == expected


def test_schema_overrides_hydra(monkeypatch: Any, tmpdir: Path) -> None:
    monkeypatch.chdir("tests/test_apps/schema-overrides-hydra")
    cmd = [
        "my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert result == "job_name: test, name: James Bond, age: 7, group: a"


def test_defaults_pkg_with_dot(monkeypatch: Any, tmpdir: Path) -> None:
    monkeypatch.chdir("tests/test_apps/defaults_pkg_with_dot")
    cmd = [
        "my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert OmegaConf.create(result) == {
        "dataset": {"test": {"name": "imagenet", "path": "/datasets/imagenet"}}
    }


class TestTaskRunnerLogging:
    def test_1(
        self, hydra_restore_singletons: Any, hydra_task_runner: TTaskRunner
    ) -> None:
        with hydra_task_runner(
            calling_file=None,
            calling_module="tests.test_apps.app_without_config.my_app",
            config_path=None,
            config_name=None,
        ):
            logger = getLogger(__name__)
            logger.info("test_1")

    def test_2(self) -> None:
        logger = getLogger(__name__)
        logger.info("test_2")


@pytest.mark.parametrize(  # type: ignore
    "expected",
    [
        (
            dedent(
                """\
                Traceback (most recent call last):
                  File "my_app.py", line 9, in my_app
                    1 / 0
                ZeroDivisionError: division by zero

                Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
                """
            )
        ),
    ],
)
def test_hydra_exception(monkeypatch: Any, tmpdir: Any, expected: str) -> None:
    monkeypatch.chdir("tests/test_apps/app_exception")
    ret = run_with_error(["my_app.py", f"hydra.run.dir={tmpdir}"])

    assert_text_same(
        from_line=expected,
        to_line=ret,
        from_name="Expected output",
        to_name="Actual output",
    )


def test_structured_with_none_list(monkeypatch: Any, tmpdir: Path) -> None:
    monkeypatch.chdir("tests/test_apps/structured_with_none_list")
    cmd = [
        "my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert result == "{'list': None}"
