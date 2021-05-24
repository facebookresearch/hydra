# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List

from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import TSweepRunner, chdir_plugin_root
from pytest import mark

from hydra_plugins.hydra_rq_launcher.rq_launcher import RQLauncher

chdir_plugin_root()


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert RQLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


# https://github.com/rq/rq/issues/1244
@mark.filterwarnings("ignore::DeprecationWarning")
@mark.parametrize("launcher_name, overrides", [("rq", [])])
class TestRQLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    """

    pass


# https://github.com/rq/rq/issues/1244
@mark.filterwarnings("ignore::DeprecationWarning")
@mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [({}, ["-m", "hydra/launcher=rq"])],
)
class TestRQLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass


# https://github.com/rq/rq/issues/1244
@mark.filterwarnings("ignore::DeprecationWarning")
@mark.parametrize("params_overrides", [[], ["hydra.launcher.redis.ssl=true"]])
def test_example_app(
    hydra_sweep_runner: TSweepRunner, params_overrides: List[str]
) -> None:
    with hydra_sweep_runner(
        calling_file="example/my_app.py",
        calling_module=None,
        task_function=None,
        config_path=".",
        config_name="config",
        overrides=["task=1,2,3,4"] + params_overrides,
    ) as sweep:
        overrides = {("task=1",), ("task=2",), ("task=3",), ("task=4",)}

        assert sweep.returns is not None and len(sweep.returns[0]) == 4
        for ret in sweep.returns[0]:
            assert tuple(ret.overrides) in overrides
