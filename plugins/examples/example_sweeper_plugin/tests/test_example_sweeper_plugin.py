# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import TSweepRunner, sweep_runner  # noqa: F401
from hydra_plugins.example_sweeper_plugin import ExampleSweeper


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking at the Sweeper plugins
    assert ExampleSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


def test_launched_jobs(sweep_runner: TSweepRunner) -> None:  # noqa: F811 # type: ignore
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs",
        config_name="compose.yaml",
        task_function=None,
        overrides=["hydra/sweeper=example", "hydra/launcher=basic", "foo=1,2"],
        strict=True,
    )
    with sweep:
        assert sweep.returns is not None
        job_ret = sweep.returns[0]
        assert len(job_ret) == 2
        assert job_ret[0].overrides == ["foo=1"]
        assert job_ret[0].cfg == {"foo": 1, "bar": 100}
        assert job_ret[1].overrides == ["foo=2"]
        assert job_ret[1].cfg == {"foo": 2, "bar": 100}
