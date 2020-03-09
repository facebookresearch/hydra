# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from typing import List

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra.test_utils.launcher_common_tests import IntegrationTestSuite
from hydra.test_utils.test_utils import integration_test


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        (
            {
                "defaults": [
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                    {"hydra/launcher": "basic"},
                ]
            },
            ["-m"],
        )
    ],
)
class TestBasicLauncherIntegration(IntegrationTestSuite):
    pass


@pytest.mark.parametrize(  # type: ignore
    "task_config, overrides, expected_dir",
    [
        ({"hydra": {"run": {"dir": "foo"}}}, [], "foo"),
        ({}, ["hydra.run.dir=bar"], "bar"),
        ({"hydra": {"run": {"dir": "foo"}}}, ["hydra.run.dir=boom"], "boom"),
        (
            {
                "hydra": {"run": {"dir": "foo-${hydra.job.override_dirname}"}},
                "app": {"a": 1, "b": 2},
            },
            ["app.a=20"],
            "foo-app.a=20",
        ),
    ],
)
def test_local_run_workdir(
    tmpdir: Path, task_config: DictConfig, overrides: List[str], expected_dir: str
) -> None:
    cfg = OmegaConf.create(task_config)
    assert isinstance(cfg, DictConfig)
    expected_dir1 = tmpdir / expected_dir
    integration_test(
        tmpdir=tmpdir,
        task_config=cfg,
        overrides=overrides,
        prints="os.getcwd()",
        expected_outputs=str(expected_dir1),
    )
