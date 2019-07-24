import pytest

from hydra.test_utils.launcher_test_common import *
# noinspection PyUnresolvedReferences
from hydra.test_utils.utils import chdir_hydra_root, sweep_runner

chdir_hydra_root()


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. https://github.com/fairinternal/submitit/issues/121")
def test_demo_6():
    demo_6_sweep_test_impl(overrides=[
        'launcher=submitit',
        'hydra.launcher.params.queue=local'
    ])


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. https://github.com/fairinternal/submitit/issues/121")
def test_fairtask_sweep_1_job(sweep_runner):
    demos_sweep_1_job_test_impl(sweep_runner, overrides=[
        'launcher=submitit',
        'hydra.launcher.params.queue=local'
    ])


@pytest.mark.skip(
    reason="submitit local queue is broken. re-enable once fixed. https://github.com/fairinternal/submitit/issues/121")
def test_fairtask_sweep_2_jobs(sweep_runner):
    demos_sweep_2_jobs_test_impl(sweep_runner, overrides=[
        'launcher=submitit',
        'hydra.launcher.params.queue=local'
    ])
