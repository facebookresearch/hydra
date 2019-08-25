# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import importlib

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import integration_test

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401


def verify_plugin(plugin_module):
    if plugin_module is not None:
        try:
            importlib.import_module(plugin_module)
        except ImportError:
            pytest.skip("Plugin {} not installed".format(plugin_module))


def create_basic_launcher_config():
    return OmegaConf.create(
        {
            "defaults": [
                {"hydra/hydra_logging": "hydra_debug"},
                {"hydra/job_logging": "disabled"},
                {"hydra/launcher": "basic"},
            ]
        }
    )


def create_fairtask_launcher_local_config():
    return OmegaConf.create(
        {
            "defaults": [
                {"hydra/launcher": None},
                {"hydra/hydra_logging": "hydra_debug"},
                {"hydra/job_logging": "disabled"},
            ],
            "hydra": {
                "launcher": {
                    "class": "hydra_plugins.fairtask.FAIRTaskLauncher",
                    "params": {
                        "no_workers": True,
                        "queue": "local",
                        "queues": {
                            "local": {
                                "class": "fairtask.local.LocalQueueConfig",
                                "params": {"num_workers": 2},
                            }
                        },
                    },
                }
            },
        }
    )


def create_submitit_launcher_local_config():
    return OmegaConf.create(
        {
            "defaults": [
                {"hydra/launcher": None},
                {"hydra/hydra_logging": "hydra_debug"},
                {"hydra/job_logging": "disabled"},
            ],
            "hydra": {
                "launcher": {
                    "class": "hydra_plugins.submitit.SubmititLauncher",
                    "params": {
                        "queue": "local",
                        "folder": "${hydra.sweep.dir}/.${hydra.launcher.params.queue}",
                        "queue_parameters": {
                            "local": {
                                "gpus_per_node": 1,
                                "tasks_per_node": 1,
                                "timeout_min": 1,
                            }
                        },
                    },
                }
            },
        }
    )


@pytest.mark.parametrize(
    "task_config, overrides, filename, expected_name",
    [
        (None, [], "no_config.py", "no_config"),
        (None, ["hydra.job.name=overridden_name"], "no_config.py", "overridden_name"),
        (
            OmegaConf.create({"hydra": {"job": {"name": "name_from_config_file"}}}),
            [],
            "with_config.py",
            "name_from_config_file",
        ),
        (
            OmegaConf.create(dict(hydra=dict(name="name_from_config_file"))),
            ["hydra.job.name=overridden_name"],
            "with_config.py",
            "overridden_name",
        ),
    ],
)
@pytest.mark.parametrize(
    "hydra_config, extra_flags, plugin_module",
    [
        (create_basic_launcher_config(), ["-m", "hydra.sweep.dir=."], None),
        (
            create_fairtask_launcher_local_config(),
            ["-m", "hydra.sweep.dir=."],
            "hydra_plugins.fairtask",
        ),
        # # TODO: re-enable after submitit local queue is fixed
        # pytest.param(
        #     create_submitit_launcher_local_config(), ['-m'], 'hydra_plugins.submitit',
        #     marks=[pytest.mark.skip]
        # ),
    ],
)
def test_custom_task_name(
    tmpdir,
    task_config,
    overrides,
    filename,
    expected_name,
    hydra_config,
    extra_flags,
    plugin_module,
):
    verify_plugin(plugin_module)
    overrides = extra_flags + overrides
    cfg = OmegaConf.merge(
        hydra_config or OmegaConf.create(), task_config or OmegaConf.create()
    )
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=overrides,
        prints="HydraConfig().hydra.job.name",
        expected_outputs=expected_name,
        filename=filename,
    )


@pytest.mark.parametrize(
    "task_config, overrides, expected_dir",
    [
        ({"hydra": {"run": {"dir": "foo"}}}, [], "foo"),
        ({}, ["hydra.run.dir=bar"], "bar"),
        ({"hydra": {"run": {"dir": "foo"}}}, ["hydra.run.dir=boom"], "boom"),
        (
            {"hydra": {"run": {"dir": "foo-${hydra.job.override_dirname}"}}},
            ["a=1", "b=2"],
            "foo-a=1,b=2",
        ),
    ],
)
def test_custom_local_run_workdir(tmpdir, task_config, overrides, expected_dir):
    cfg = OmegaConf.create(task_config)
    expected_dir1 = tmpdir / expected_dir
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=overrides,
        prints="os.getcwd()",
        expected_outputs=str(expected_dir1),
    )


@pytest.mark.parametrize(
    "task_config, overrides, expected_dir",
    [
        (
            {
                "hydra": {
                    "sweep": {"dir": "task_cfg", "subdir": "task_cfg_${hydra.job.num}"}
                }
            },
            [],
            "task_cfg/task_cfg_0",
        ),
        (
            {},
            ["hydra.sweep.dir=cli_dir", "hydra.sweep.subdir=cli_dir_${hydra.job.num}"],
            "cli_dir/cli_dir_0",
        ),
        (
            {
                "hydra": {
                    "sweep": {"dir": "task_cfg", "subdir": "task_cfg_${hydra.job.num}"}
                }
            },
            ["hydra.sweep.dir=cli_dir", "hydra.sweep.subdir=cli_dir_${hydra.job.num}"],
            "cli_dir/cli_dir_0",
        ),
        (
            {
                "hydra": {
                    "sweep": {
                        "dir": "hydra_cfg",
                        "subdir": "${hydra.job.override_dirname}",
                    }
                }
            },
            ["a=1", "b=2"],
            "hydra_cfg/a=1,b=2",
        ),
    ],
)
@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags, plugin_module",
    [
        (create_basic_launcher_config(), ["-m"], None),
        (create_fairtask_launcher_local_config(), ["-m"], "hydra_plugins.fairtask"),
        # TODO: re-enable after submitit local queue is fixed
        pytest.param(
            create_submitit_launcher_local_config(),
            ["-m"],
            "hydra_plugins.submitit",
            marks=[pytest.mark.skip],
        ),
    ],
)
def test_custom_sweeper_run_workdir(
    tmpdir,
    task_config,
    overrides,
    expected_dir,
    task_launcher_cfg,
    extra_flags,
    plugin_module,
):
    verify_plugin(plugin_module)
    if task_config is not None:
        task_config = OmegaConf.create(task_config)

    overrides = extra_flags + overrides
    cfg = OmegaConf.merge(task_launcher_cfg, task_config)

    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=overrides,
        prints="os.getcwd()",
        expected_outputs=str(tmpdir / expected_dir),
    )
