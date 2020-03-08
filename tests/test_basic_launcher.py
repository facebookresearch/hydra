# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra.test_utils.launcher_common_tests import (
    BatchedSweeperTestSuite,
    IntegrationTestSuite,
    LauncherTestSuite,
)

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401


@pytest.mark.parametrize("launcher_name, overrides", [("basic", [])])
class TestBasicLauncher(LauncherTestSuite):
    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        (
            {
                "defaults": [
                    {"hydra/launcher": "basic"},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ]
            },
            ["-m"],
        )
    ],
)
class TestExampleLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass


@pytest.mark.parametrize(
    "launcher_name, overrides",
    [("basic", ["hydra/sweeper=basic", "hydra.sweeper.params.max_batch_size=2"])],
)
class TestExampleSweeperWithBatching(BatchedSweeperTestSuite):
    ...
