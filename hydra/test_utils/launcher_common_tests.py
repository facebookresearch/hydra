# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Common test functions testing launchers
"""

import subprocess
import sys

from omegaconf import OmegaConf

from hydra.test_utils.test_utils import verify_dir_outputs


def demo_6_sweep_test_impl(tmpdir, overrides):
    """
    Runs a sweep with the config from demo 6
    """
    cmd = [sys.executable, "demos/6_sweep/experiment.py"]
    cmd.extend(
        [
            "--sweep",
            "hydra.launcher.params.queue=local",
            "hydra.sweep.dir={}".format(str(tmpdir)),
            "hydra.sweep.subdir=${hydra.job.num}",
        ]
    )
    cmd.extend(overrides)
    subprocess.check_call(cmd)


def demos_sweep_1_job_test_impl(sweep_runner, overrides, strict=False):
    """
    Runs a sweep with one job
    """
    sweep = sweep_runner(
        calling_file="demos/6_sweep/experiment.yaml",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=overrides,
        strict=strict,
    )
    with sweep:
        job_ret = sweep.returns[0]
        assert len(job_ret) == 1
        assert job_ret[0].overrides == []
        assert job_ret[0].cfg == dict(optimizer=dict(type="nesterov", lr=0.001))
        assert job_ret[0].hydra_cfg.hydra.job.name == "experiment"
        verify_dir_outputs(sweep.returns[0][0])


def demos_sweep_2_jobs_test_impl(sweep_runner, overrides):
    """
    Runs a sweep with two jobs
    """
    overrides.append("a=0,1")
    sweep = sweep_runner(
        calling_file="demos/6_sweep/experiment.yaml",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=overrides,
    )
    base = OmegaConf.create(dict(optimizer=dict(type="nesterov", lr=0.001)))

    with sweep:
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            expected_conf = OmegaConf.merge(
                base, OmegaConf.from_dotlist(job_ret.overrides)
            )
            assert job_ret.overrides == ["a={}".format(i)]
            assert job_ret.cfg == expected_conf
            assert job_ret.hydra_cfg.hydra.job.name == "experiment"
            verify_dir_outputs(job_ret, job_ret.overrides)


def not_sweeping_hydra_overrides(sweep_runner, overrides):
    """
    Runs a sweep with two jobs
    """
    overrides.extend(["a=0,1", "hydra.foo=1,2,3"])
    sweep = sweep_runner(
        calling_file="demos/6_sweep/experiment.yaml",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=overrides,
    )
    base = OmegaConf.create(dict(optimizer=dict(type="nesterov", lr=0.001)))

    with sweep:
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            expected_conf = OmegaConf.merge(
                base, OmegaConf.from_dotlist(job_ret.overrides)
            )
            assert job_ret.overrides == ["a={}".format(i)]
            assert job_ret.cfg == expected_conf
            verify_dir_outputs(job_ret, job_ret.overrides)


def sweep_over_two_optimizers(sweep_runner, overrides):
    """
    Make sure that optimizers=adam,nesterov is interpreted correctly
    """
    overrides.extend(["optimizer=adam,nesterov"])
    sweep = sweep_runner(
        calling_file="demos/6_sweep/experiment.yaml",
        calling_module=None,
        config_path="conf/config.yaml",
        overrides=overrides,
    )
    expected_overrides = [["optimizer=adam"], ["optimizer=nesterov"]]
    expected_conf = [
        OmegaConf.create(dict(optimizer=dict(type="adam", lr=0.1, beta=0.01))),
        OmegaConf.create(dict(optimizer=dict(type="nesterov", lr=0.001))),
    ]
    with sweep:
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            assert job_ret.overrides == expected_overrides[i]
            assert job_ret.cfg == expected_conf[i]
            verify_dir_outputs(job_ret, job_ret.overrides)
