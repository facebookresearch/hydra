# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra.test_utils.launcher_common_tests import (
    demo_6_sweep_test_impl,
    demos_sweep_1_job_test_impl,
    demos_sweep_2_jobs_test_impl,
    not_sweeping_hydra_overrides,
    sweep_over_two_optimizers,
)

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import chdir_hydra_root, sweep_runner  # noqa: F401

chdir_hydra_root()


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. "
    "https://github.com/fairinternal/submitit/issues/121"
)
def test_demo_6(tmpdir):
    demo_6_sweep_test_impl(
        tmpdir, overrides=["launcher=submitit", "hydra.launcher.params.queue=local"]
    )


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. "
    "https://github.com/fairinternal/submitit/issues/121"
)
def test_fairtask_sweep_1_job(sweep_runner):  # noqa: F811
    demos_sweep_1_job_test_impl(
        sweep_runner,
        overrides=["launcher=submitit", "hydra.launcher.params.queue=local"],
    )


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. "
    "https://github.com/fairinternal/submitit/issues/121"
)
def test_fairtask_sweep_2_jobs(sweep_runner):  # noqa: F811
    demos_sweep_2_jobs_test_impl(
        sweep_runner,
        overrides=["launcher=submitit", "hydra.launcher.params.queue=local"],
    )


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. "
    "https://github.com/fairinternal/submitit/issues/121"
)
def test_not_sweeping_hydra_overrides(sweep_runner):  # noqa: F811
    not_sweeping_hydra_overrides(
        sweep_runner,
        overrides=["launcher=submitit", "hydra.launcher.params.queue=local"],
    )


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. "
    "https://github.com/fairinternal/submitit/issues/121"
)
def test_fairtask_sweep_2_optimizers(sweep_runner):  # noqa: F811
    sweep_over_two_optimizers(
        sweep_runner,
        overrides=["launcher=submitit", "hydra.launcher.params.queue=local"],
    )
