from hydra.test_utils.launcher_test_common import demos_sweep_1_job_test_impl, demos_sweep_2_jobs_test_impl
# noinspection PyUnresolvedReferences
from hydra.test_utils.utils import chdir_hydra_root, sweep_runner

chdir_hydra_root()


def test_fairtask_sweep_1_job(sweep_runner):
    demos_sweep_1_job_test_impl(sweep_runner, overrides=[
        'launcher=fairtask',
        'hydra.launcher.params.queue=local',
        'hydra.launcher.params.no_workers=true'
    ])


def test_fairtask_sweep_2_jobs(sweep_runner):
    demos_sweep_2_jobs_test_impl(sweep_runner, overrides=[
        'launcher=fairtask',
        'hydra.launcher.params.queue=local',
        'hydra.launcher.params.no_workers=true'
    ])
