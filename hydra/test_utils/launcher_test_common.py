"""
Common test functions testing launchers
"""

import shutil
import subprocess
import sys
import tempfile

from omegaconf import OmegaConf

from hydra.test_utils.test_utils import verify_dir_outputs


def demo_6_sweep_test_impl(overrides):
    """
    Runs a sweep with the config from demo 6
    """
    cmd = [sys.executable, 'demos/6_sweep/experiment.py']
    try:
        tempdir = tempfile.mkdtemp()
        cmd.extend([
            '--sweep',
            'hydra.launcher.params.queue=local',
            'hydra.sweep.dir={}'.format(tempdir),
            'hydra.sweep.subdir=${job:num}',
        ])
        cmd.extend(overrides)
        result = subprocess.check_output(cmd)
        lines = str.splitlines(result.decode('utf-8'))
        print(lines)
    finally:
        shutil.rmtree(tempdir)


def demos_sweep_1_job_test_impl(sweep_runner, overrides):
    """
    Runs a sweep with one job
    """
    sweep = sweep_runner(conf_dir='demos/6_sweep/conf/',
                         conf_filename='config.yaml',
                         overrides=overrides)
    with sweep:
        job_ret = sweep.returns[0]
        assert len(job_ret) == 1
        assert job_ret[0].overrides == []
        # delete the hydra node added by the sweep tester
        del job_ret[0].cfg['hydra']
        assert job_ret[0].cfg == dict(
            optimizer=dict(
                type='nesterov',
                lr=0.001,
            ),
        )
        verify_dir_outputs(sweep.returns[0][0].working_dir)


def demos_sweep_2_jobs_test_impl(sweep_runner, overrides):
    """
    Runs a sweep with two jobs
    """
    overrides.append('a=0,1')
    sweep = sweep_runner(conf_dir='demos/6_sweep/conf/',
                         conf_filename='config.yaml',
                         overrides=overrides)
    base = OmegaConf.create(dict(
        optimizer=dict(
            type='nesterov',
            lr=0.001,
        ),
    ))

    with sweep:
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            expected_conf = OmegaConf.merge(
                base, OmegaConf.from_dotlist(
                    job_ret.overrides))
            assert job_ret.overrides == ['a={}'.format(i)]
            del job_ret.cfg['hydra']
            assert job_ret.cfg == expected_conf
            verify_dir_outputs(job_ret.working_dir, job_ret.overrides)
