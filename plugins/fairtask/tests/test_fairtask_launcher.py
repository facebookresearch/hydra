from hydra.test_utils.launcher_test_common import demos_sweep_1_job_test_impl, \
    demos_sweep_2_jobs_test_impl, demo_6_sweep_test_impl
# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import chdir_hydra_root, sweep_runner  # noqa: F401

chdir_hydra_root()


def test_demo_6():
    demo_6_sweep_test_impl(overrides=[
        'launcher=fairtask',
        'hydra.launcher.params.queue=local',
        'hydra.launcher.params.no_workers=true'
    ])


def test_fairtask_sweep_1_job(sweep_runner):  # noqa: F811
    demos_sweep_1_job_test_impl(sweep_runner, overrides=[
        'launcher=fairtask',
        'hydra.launcher.params.queue=local',
        'hydra.launcher.params.no_workers=true'
    ])


def test_fairtask_sweep_2_jobs(sweep_runner):  # noqa: F811
    demos_sweep_2_jobs_test_impl(sweep_runner, overrides=[
        'launcher=fairtask',
        'hydra.launcher.params.queue=local',
        'hydra.launcher.params.no_workers=true'
    ])
