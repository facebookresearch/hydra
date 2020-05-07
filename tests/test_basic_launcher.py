# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra.test_utils.launcher_common_tests import (
    BatchedSweeperTestSuite,
    IntegrationTestSuite,
    LauncherTestSuite,
)


@pytest.mark.parametrize("launcher_name, overrides", [("basic", [])])
class TestBasicLauncher(LauncherTestSuite):
    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        pytest.param(
            {
                "defaults": [
                    {"hydra/launcher": "basic"},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ]
            },
            ["-m"],
            id="basic_launcher_multirun",
        )
    ],
)
class TestBasicLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass


@pytest.mark.parametrize(
    "launcher_name, overrides",
    [("basic", ["hydra/sweeper=basic", "hydra.sweeper.params.max_batch_size=2"])],
)
class TestBasicSweeperWithBatching(BatchedSweeperTestSuite):
    ...
