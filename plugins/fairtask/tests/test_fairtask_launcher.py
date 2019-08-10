# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys

import pytest

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


@pytest.mark.parametrize('filename, args, expected_name', [
    ('no_config_file_override.py', [], 'no_config_file_override'),
    ('no_config_file_override.py', ['hydra.name=overridden_name'], 'overridden_name'),
    ('with_config_file_override.py', [], 'name_from_config_file'),
    ('with_config_file_override.py', ['hydra.name=overridden_name'], 'overridden_name'),
])
def test_demo_99_task_name(filename, args, expected_name):
    cmd = [
        sys.executable,
        'demos/99_hydra_configuration/task_name/' + filename
    ]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert result.decode('utf-8') == expected_name + "\n"
