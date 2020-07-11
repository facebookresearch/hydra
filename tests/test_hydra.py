# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Optional, Set

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra import MissingConfigException
from hydra.test_utils.test_utils import (
    TSweepRunner,
    TTaskRunner,
    chdir_hydra_root,
    integration_test,
    verify_dir_outputs,
)
from tests import normalize_newlines
from tests.test_examples import run_with_error

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
    )
    with task:
        assert task.job_ret is not None and task.job_ret.cfg == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }

        verify_dir_outputs(task.job_ret)


@pytest.mark.parametrize(  # type: ignore
    "calling_file, calling_module",
    [
        ("tests/test_apps/app_with_cfg_groups_no_header/my_app.py", None,),
        (None, "tests.test_apps.app_with_cfg_groups_no_header.my_app",),
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
        "\nSee https://hydra.cc/next/upgrades/0.11_to_1.0/config_path_changes"
    )

    with pytest.warns(expected_warning=UserWarning, match=re.escape(msg)):
        task = hydra_task_runner(
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
            hydra_cfg.hydra.launcher.target
            == "hydra._internal.core_plugins.basic_launcher.BasicLauncher"
        )
        assert len(task.job_ret.hydra_cfg.hydra.launcher.params) == 0


def test_short_module_name(tmpdir: Path) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result = subprocess.check_output(cmd)
    assert OmegaConf.create(str(result.decode("utf-8"))) == {
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
        sys.executable,
        "examples/tutorials/basic/your_first_hydra_app/2_config_file/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    modified_env = os.environ.copy()
    modified_env[env_name] = "hydra.test_utils.configs.Foo"
    result = subprocess.check_output(cmd, env=modified_env)
    assert OmegaConf.create(str(result.decode("utf-8"))) == {"normal_yaml_config": True}


@pytest.mark.parametrize(  # type: ignore
    "flag,expected_keys",
    [("--cfg=all", ["db", "hydra"]), ("--cfg=hydra", ["hydra"]), ("--cfg=job", ["db"])],
)
def test_cfg(tmpdir: Path, flag: str, expected_keys: List[str]) -> None:
    cmd = [
        sys.executable,
        "examples/tutorials/basic/your_first_hydra_app/5_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        flag,
    ]
    result = subprocess.check_output(cmd)
    conf = OmegaConf.create(str(result.decode("utf-8")))
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
        sys.executable,
        "examples/tutorials/basic/your_first_hydra_app/5_defaults/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ] + flags

    result = subprocess.check_output(cmd).decode("utf-8")
    assert normalize_newlines(result) == expected


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
--version : show program's version number and exit
--cfg,-c : Show config instead of running [job|hydra|all]
--package,-p : Config package to show
--run,-r : Run a job
--multirun,-m : Run multiple jobs with the configured launcher
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
--version : show program's version number and exit
--cfg,-c : Show config instead of running [job|hydra|all]
--package,-p : Config package to show
--run,-r : Run a job
--multirun,-m : Run multiple jobs with the configured launcher
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
--info,-i : Print Hydra information
Overrides : Any key=value arguments to override config values (use dots for.nested=overrides)
""",
            id="overriding_hydra_help_template:$FLAGS_HELP",
        ),
    ],
)
def test_help(
    tmpdir: Path, script: str, flag: str, overrides: List[str], expected: Any,
) -> None:
    cmd = [sys.executable, script, "hydra.run.dir=" + str(tmpdir)]
    cmd.extend(overrides)
    cmd.append(flag)
    print(" ".join(cmd))
    result = str(subprocess.check_output(cmd).decode("utf-8"))
    # normalize newlines on Windows to make testing easier
    result = result.replace("\r\n", "\n")
    assert result == expected.format(script=script)


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


def test_hydra_env_set(tmpdir: Path) -> None:
    cfg = OmegaConf.create({"hydra": {"job": {"env_set": {"foo": "bar"}}}})
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=[],
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
        sys.executable,
        "tests/test_apps/app_with_multiple_config_dirs/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        f"--config-name={config_name}",
        f"--config-path={config_path}",
    ]
    print(" ".join(cmd))
    result = str(subprocess.check_output(cmd).decode("utf-8")).strip()
    # normalize newlines on Windows to make testing easier
    result = result.replace("\r\n", "\n")
    assert result == f"{config_path}_{config_name}: true"


@pytest.mark.parametrize(  # type: ignore
    "overrides, expected_files",
    [
        ([], {"my_app.log", ".hydra"}),
        (["hydra.output_subdir=foo"], {"my_app.log", "foo"}),
        (["hydra.output_subdir=null"], {"my_app.log"}),
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
        ("tests/test_apps/run_as_module/1", "my_app.py", "my_app", "Empty module name"),
        ("tests/test_apps/run_as_module/2", "my_app.py", "my_app", None),
        ("tests/test_apps/run_as_module/3", "module/my_app.py", "module.my_app", None),
        ("tests/test_apps/run_as_module/4", "module/my_app.py", "module.my_app", None),
    ],
)
def test_module_run(
    tmpdir: Any, directory: str, file: str, module: str, error: Optional[str]
) -> None:
    cmd = [
        sys.executable,
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
        result = subprocess.check_output(cmd, env=modified_env)
        assert OmegaConf.create(str(result.decode("utf-8"))) == {"x": 10}


@pytest.mark.parametrize(  # type: ignore
    "overrides,error,expected",
    [
        pytest.param(["test.param=1"], False, "1", id="run:value"),
        pytest.param(
            ["test.param=1,2"],
            True,
            """Ambiguous value for argument 'test.param=1,2'
1. To use it as a list, use test.param=[1,2]
2. To use it as string use test.param=\\'1,2\\'
3. To sweep over it, add --multirun to your command line

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.""",
            id="run:choice_sweep",
        ),
        pytest.param(["test.param=[1,2]"], False, "[1, 2]", id="run:list_value"),
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
        sys.executable,
        "tests/test_apps/multirun_structured_conflict/my_app.py",
        "hydra.sweep.dir=" + str(tmpdir),
    ]
    cmd.extend(overrides)
    if error:
        ret = run_with_error(cmd)
        assert re.search(re.escape(expected), ret) is not None
    else:
        ret = normalize_newlines(
            str(subprocess.check_output(cmd).decode("utf-8"))
        ).strip()
        assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "sweep", [pytest.param(False, id="run"), pytest.param(True, id="sweep")]
)
def test_run_with_missing_default(tmpdir: Any, sweep: bool) -> None:
    cmd = [
        sys.executable,
        "tests/test_apps/simple_app/my_app.py",
        "--config-name=unspecified_mandatory_default",
        "--config-path=../../../hydra/test_utils/configs",
        "hydra/hydra_logging=disabled",
        "hydra.sweep.dir=" + str(tmpdir),
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
