# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.test_utils.launcher_common_tests import (
    BatchedSweeperTestSuite,
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import TSweepRunner

from hydra_plugins.example_sweeper_plugin.example_sweeper import ExampleSweeper


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking at the Sweeper plugins
    assert ExampleSweeper.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Sweeper)
    ]


def test_launched_jobs(hydra_sweep_runner: TSweepRunner) -> None:
    sweep = hydra_sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs",
        config_name="compose.yaml",
        task_function=None,
        overrides=["hydra/sweeper=example", "hydra/launcher=basic", "foo=1,2"],
    )
    with sweep:
        assert sweep.returns is not None
        job_ret = sweep.returns[0]
        assert len(job_ret) == 2
        assert job_ret[0].overrides == ["foo=1"]
        assert job_ret[0].cfg == {"foo": 1, "bar": 100}
        assert job_ret[1].overrides == ["foo=2"]
        assert job_ret[1].cfg == {"foo": 2, "bar": 100}


# Run launcher test suite with the basic launcher and this sweeper
@pytest.mark.parametrize(
    "launcher_name, overrides",
    [
        (
            "basic",
            [
                # CHANGE THIS TO YOUR SWEEPER CONFIG NAME
                "hydra/sweeper=example"
            ],
        )
    ],
)
class TestExampleSweeper(LauncherTestSuite):
    ...


# Many sweepers are batching jobs in groups.
# This test suite verifies that the spawned jobs are not overstepping the directories of one another.
@pytest.mark.parametrize(
    "launcher_name, overrides",
    [
        (
            "basic",
            [
                # CHANGE THIS TO YOUR SWEEPER CONFIG NAME
                "hydra/sweeper=example",
                # This will cause the sweeper to split batches to at most 2 jobs each, which is what
                # the tests in BatchedSweeperTestSuite are expecting.
                "hydra.sweeper.max_batch_size=2",
            ],
        )
    ],
)
class TestExampleSweeperWithBatching(BatchedSweeperTestSuite):
    ...


# Run integration test suite with the basic launcher and this sweeper
@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        (
            {},
            [
                "-m",
                # CHANGE THIS TO YOUR SWEEPER CONFIG NAME
                "hydra/sweeper=example",
                "hydra/launcher=basic",
            ],
        )
    ],
)
class TestExampleSweeperIntegration(IntegrationTestSuite):
    pass
