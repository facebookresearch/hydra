"""
Common test functions testing launchers
"""

import shutil
import subprocess
import sys
import tempfile

from omegaconf import OmegaConf

# noinspection PyUnresolvedReferences
from hydra.test_utils.utils import task_runner, sweep_runner, chdir_hydra_root, verify_dir_outputs
from hydra.test_utils.utils import verify_dir_outputs


def demo_6_sweep_test_impl(overrides):
    cmd = [sys.executable, 'demos/6_sweep/sweep_example.py']
    try:
        tempdir = tempfile.mkdtemp()
        cmd.extend([
            '--sweep',
            'hydra.launcher.params.queue=local',
            'hydra.sweep.dir={}'.format(tempdir),
            'hydra.sweep.subdir=${job:num}'
        ])
        cmd.extend(overrides)
        result = subprocess.check_output(cmd)
        lines = str.splitlines(result.decode('utf-8'))
        print(lines)
    finally:
        shutil.rmtree(tempdir)


def demos_sweep_1_job_test_impl(sweep_runner, overrides):
    sweep = sweep_runner(conf_dir='demos/6_sweep/conf/',
                         conf_filename='config.yaml',
                         overrides=overrides)
    with sweep:
        assert len(sweep.returns) == 1
        assert sweep.returns[0].overrides == []
        assert sweep.returns[0].cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet'
            ),
            model=dict(
                type='alexnet',
                num_layers=7
            ),
            optimizer=dict(
                type='nesterov',
                lr=0.001,
            ),
        )
        verify_dir_outputs(sweep.returns[0].working_dir)


def demos_sweep_2_jobs_test_impl(sweep_runner, overrides):
    overrides.append('a=0,1')
    sweep = sweep_runner(conf_dir='demos/6_sweep/conf/',
                         conf_filename='config.yaml',
                         overrides=overrides)
    base = OmegaConf.create(dict(
        dataset=dict(
            name='imagenet',
            path='/datasets/imagenet'
        ),
        model=dict(
            type='alexnet',
            num_layers=7
        ),
        optimizer=dict(
            type='nesterov',
            lr=0.001,
        ),
    ))

    with sweep:
        assert len(sweep.returns) == 2
        for i in range(2):
            job_ret = sweep.returns[i]
            expected_conf = OmegaConf.merge(base, OmegaConf.from_dotlist(job_ret.overrides))
            assert job_ret.overrides == ['a={}'.format(i)]
            assert job_ret.cfg == expected_conf
            verify_dir_outputs(job_ret.working_dir, job_ret.overrides)
