# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra.test_utils.launcher_test_common import demos_sweep_1_job_test_impl, \
    demos_sweep_2_jobs_test_impl, demo_6_sweep_test_impl, demo_99_task_name_impl
# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import chdir_hydra_root, sweep_runner  # noqa: F401

chdir_hydra_root()


def test_demo_6(tmpdir):
    demo_6_sweep_test_impl(
        tmpdir,
        overrides=[
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


@pytest.mark.parametrize('conf_dir, conf_file, overrides, expected_name', [
    ('demos/99_hydra_configuration/task_name/', None, [], 'no_config_file_override'),
    ('demos/99_hydra_configuration/task_name/', None, ['hydra.name=overridden_name'],
     'overridden_name'),
    ('demos/99_hydra_configuration/task_name/', 'config.yaml', [], 'name_from_config_file'),
    ('demos/99_hydra_configuration/task_name/', 'config.yaml', ['hydra.name=overridden_name'],
     'overridden_name'),
])
def test_task_name(sweep_runner, conf_dir, conf_file, overrides, expected_name):
    demo_99_task_name_impl(sweep_runner, conf_dir, conf_file, overrides, expected_name, overrides=[
        'launcher=fairtask',
        'hydra.launcher.params.queue=local',
        'hydra.launcher.params.no_workers=true'
    ])
