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


def create_fairtask_launcher_local_config():
    return OmegaConf.create(
        {
            "hydra": {
                "hydra_logging": {"root": {"level": "ERROR"}},
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
                },
            }
        }
    )


def create_submitit_launcher_local_config():
    return OmegaConf.create(
        {
            "hydra": {
                "hydra_logging": {"root": {"level": "ERROR"}},
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
                },
            }
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
        (None, [], None),
        (
            create_fairtask_launcher_local_config(),
            ["-s", "hydra.sweep.dir=."],
            "hydra_plugins.fairtask",
        ),
        # # TODO: re-enable after submitit local queue is fixed
        # pytest.param(
        #     create_submitit_launcher_local_config(), ['-s'], 'hydra_plugins.submitit',
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
        tmpdir,
        task_config=cfg,
        hydra_config=None,
        overrides=overrides,
        prints="HydraConfig().hydra.job.name",
        expected_outputs=expected_name,
        filename=filename,
    )


@pytest.mark.parametrize(
    "task_config, hydra_cfg, overrides, expected_dir",
    [
        # test with task config override
        (OmegaConf.create({"hydra": {"run": {"dir": "foo"}}}), {}, [], "foo"),
        # test with command line override
        ({}, {}, ["hydra.run.dir=bar"], "bar"),
        # test with both task config and command line override
        (
            OmegaConf.create({"hydra": {"run": {"dir": "foo"}}}),
            {},
            ["hydra.run.dir=boom"],
            "boom",
        ),
        # hydra config override
        # test with task config override
        ({}, OmegaConf.create({"hydra": {"run": {"dir": "foo"}}}), [], "foo"),
        (
            {},
            OmegaConf.create({"hydra": {"run": {"dir": "abc"}}}),
            ["hydra.run.dir=efg"],
            "efg",
        ),
        # test with both task config and command line override
        (
            {},
            OmegaConf.create({"hydra": {"run": {"dir": "abc"}}}),
            ["hydra.run.dir=efg"],
            "efg",
        ),
        (
            OmegaConf.create({"hydra": {"run": {"dir": "abc"}}}),
            OmegaConf.create({"hydra": {"run": {"dir": "def"}}}),
            ["hydra.run.dir=boom"],
            "boom",
        ),
    ],
)
def test_custom_local_run_workdir(
    tmpdir, task_config, hydra_cfg, overrides, expected_dir
):
    cfg = OmegaConf.merge(task_config or OmegaConf.create())

    expected_dir1 = tmpdir / expected_dir
    integration_test(
        tmpdir,
        task_config=cfg,
        hydra_config=hydra_cfg,
        overrides=overrides,
        prints="os.getcwd()",
        expected_outputs=str(expected_dir1),
    )


@pytest.mark.parametrize(
    "task_config, hydra_cfg, overrides, expected_dir",
    [
        (
            {
                "hydra": {
                    "sweep": {"dir": "task_cfg", "subdir": "task_cfg_${hydra.job.num}"}
                }
            },
            {},
            [],
            "task_cfg/task_cfg_0",
        ),
        (
            {},
            {
                "hydra": {
                    "sweep": {
                        "dir": "hydra_cfg",
                        "subdir": "hydra_cfg_${hydra.job.num}",
                    }
                }
            },
            [],
            "hydra_cfg/hydra_cfg_0",
        ),
        (
            {},
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
            {
                "hydra": {
                    "sweep": {
                        "dir": "hydra_cfg",
                        "subdir": "hydra_cfg_${hydra.job.num}",
                    }
                }
            },
            [],
            "task_cfg/task_cfg_0",
        ),
        (
            {
                "hydra": {
                    "sweep": {"dir": "task_cfg", "subdir": "task_cfg_${hydra.job.num}"}
                }
            },
            {},
            ["hydra.sweep.dir=cli_dir", "hydra.sweep.subdir=cli_dir_${hydra.job.num}"],
            "cli_dir/cli_dir_0",
        ),
        (
            {},
            {
                "hydra": {
                    "sweep": {
                        "dir": "hydra_cfg",
                        "subdir": "hydra_cfg_${hydra.job.num}",
                    }
                }
            },
            ["hydra.sweep.dir=cli_dir", "hydra.sweep.subdir=cli_dir_${hydra.job.num}"],
            "cli_dir/cli_dir_0",
        ),
        (
            {
                "hydra": {
                    "sweep": {"dir": "task_cfg", "subdir": "task_cfg_${hydra.job.num}"}
                }
            },
            {
                "hydra": {
                    "sweep": {
                        "dir": "hydra_cfg",
                        "subdir": "hydra_cfg_${hydra.job.num}",
                    }
                }
            },
            ["hydra.sweep.dir=cli_dir", "hydra.sweep.subdir=cli_dir_${hydra.job.num}"],
            "cli_dir/cli_dir_0",
        ),
    ],
)
@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags, plugin_module",
    [
        (create_fairtask_launcher_local_config(), ["-s"], "hydra_plugins.fairtask"),
        # TODO: re-enable after submitit local queue is fixed
        pytest.param(
            create_submitit_launcher_local_config(),
            ["-s"],
            "hydra_plugins.submitit",
            marks=[pytest.mark.skip],
        ),
    ],
)
def test_custom_sweeper_run_workdir(
    tmpdir,
    task_config,
    hydra_cfg,
    overrides,
    expected_dir,
    task_launcher_cfg,
    extra_flags,
    plugin_module,
):
    verify_plugin(plugin_module)
    if task_config is not None:
        task_config = OmegaConf.create(task_config)
    if hydra_cfg is not None:
        hydra_cfg = OmegaConf.create(hydra_cfg)

    overrides = extra_flags + overrides
    cfg = OmegaConf.merge(task_launcher_cfg, task_config)

    integration_test(
        tmpdir,
        task_config=cfg,
        hydra_config=hydra_cfg,
        overrides=overrides,
        prints="os.getcwd()",
        expected_outputs=str(tmpdir / expected_dir),
    )
