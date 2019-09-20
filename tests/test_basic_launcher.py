# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra.test_utils.launcher_common_tests import LauncherTestSuite
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401


@pytest.mark.parametrize("launcher_name, overrides", [("basic", [])])
class TestBasicLauncher(LauncherTestSuite):
    pass
