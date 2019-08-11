# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra.test_utils.launcher_common_tests import (
    demos_sweep_1_job_test_impl,
    demos_sweep_2_jobs_test_impl,
    demo_6_sweep_test_impl,
    not_sweeping_hydra_overrides,
)
from hydra.test_utils.test_utils import chdir_hydra_root

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401

chdir_hydra_root()


def test_demo_6(tmpdir):
    demo_6_sweep_test_impl(
        tmpdir,
        overrides=[
            "launcher=fairtask",
            "hydra.launcher.params.queue=local",
            "hydra.launcher.params.no_workers=true",
        ],
    )


def test_fairtask_sweep_1_job(sweep_runner):  # noqa: F811
    demos_sweep_1_job_test_impl(
        sweep_runner,
        overrides=[
            "launcher=fairtask",
            "hydra.launcher.params.queue=local",
            "hydra.launcher.params.no_workers=true",
        ],
    )


def test_fairtask_sweep_2_jobs(sweep_runner):  # noqa: F811
    demos_sweep_2_jobs_test_impl(
        sweep_runner,
        overrides=[
            "launcher=fairtask",
            "hydra.launcher.params.queue=local",
            "hydra.launcher.params.no_workers=true",
        ],
    )


def test_not_sweeping_hydra_overrides(sweep_runner):  # noqa: F811
    not_sweeping_hydra_overrides(
        sweep_runner,
        overrides=[
            "launcher=fairtask",
            "hydra.launcher.params.queue=local",
            "hydra.launcher.params.no_workers=true",
        ],
    )
