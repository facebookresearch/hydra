# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_plugin_root
from omegaconf import OmegaConf
from pytest import mark

from hydra_plugins.hydra_ray_launcher import _core_aws
from hydra_plugins.hydra_ray_launcher.ray_aws_launcher import RayAWSLauncher
from hydra_plugins.hydra_ray_launcher.ray_launcher import RayLauncher

chdir_plugin_root()

win_msg = "Ray doesn't support Windows."


@mark.skipif(sys.platform.startswith("win"), reason=win_msg)
def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert RayLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@mark.parametrize("launcher_name, overrides", [("ray", [])])
class TestRayLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    """

    pass


@mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        (
            {},
            [
                "-m",
                "hydra/launcher=ray",
                "hydra/hydra_logging=hydra_debug",
                "hydra/job_logging=disabled",
            ],
        )
    ],
)
class TestRayLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass


def test_ray_aws_launch_does_not_mutate_launcher_config(
    monkeypatch: Any, tmp_path: Path
) -> None:
    cfg = OmegaConf.create(
        {
            "env_setup": {
                "commands": ["base"],
                "pip_packages": {"example": "1.0"},
            },
            "ray": {"cluster": {"setup_commands": ["cluster"]}},
            "logging": {},
            "hydra": {
                "hydra_logging": {},
                "verbose": False,
                "sweep": {"dir": str(tmp_path)},
            },
        }
    )
    original = OmegaConf.to_container(cfg, resolve=False)
    launcher = cast(
        RayAWSLauncher,
        SimpleNamespace(
            config=cfg,
            env_setup=cfg.env_setup,
            hydra_context=object(),
            logging=cfg.logging,
            ray_cfg=cfg.ray,
            task_function=lambda: None,
        ),
    )
    captured: dict[str, Any] = {}

    monkeypatch.setattr(_core_aws, "configure_log", lambda *args: None)
    monkeypatch.setattr(_core_aws.sdk, "configure_logging", lambda **kwargs: None)
    monkeypatch.setattr(_core_aws, "_pickle_jobs", lambda **kwargs: None)

    def launch_jobs(
        launcher: Any,
        local_tmp_dir: str,
        sweep_dir: Path,
        ray_cluster: Any,
    ) -> list[Any]:
        captured["ray_cluster"] = ray_cluster
        return []

    monkeypatch.setattr(_core_aws, "launch_jobs", launch_jobs)

    assert _core_aws.launch(launcher, [], 0) == []
    assert OmegaConf.to_container(cfg, resolve=False) == original
    assert captured["ray_cluster"].setup_commands == [
        "base",
        "pip install example==1.0",
        "cluster",
    ]
