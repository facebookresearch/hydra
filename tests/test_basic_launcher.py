# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import mark, param

from hydra.test_utils.launcher_common_tests import (
    BatchedSweeperTestSuite,
    IntegrationTestSuite,
    LauncherTestSuite,
)


@mark.parametrize("launcher_name, overrides", [("basic", [])])
class TestBasicLauncher(LauncherTestSuite):
    pass


@mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        param(
            {},
            [
                "-m",
                "hydra/launcher=basic",
                "hydra/hydra_logging=disabled",
                "hydra/job_logging=disabled",
            ],
            id="basic_launcher_multirun",
        )
    ],
)
class TestBasicLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass


@mark.parametrize(
    "launcher_name, overrides",
    [
        (
            "basic",
            [
                "hydra/sweeper=basic",
                "hydra.sweeper.max_batch_size=2",
            ],
        )
    ],
)
class TestBasicSweeperWithBatching(BatchedSweeperTestSuite): ...
