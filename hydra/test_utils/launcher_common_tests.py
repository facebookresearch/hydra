# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Common test functions testing launchers
"""

import subprocess
import sys

import pytest

from hydra.test_utils.test_utils import verify_dir_outputs
from omegaconf import OmegaConf


class LauncherTestSuite:
    def test_demo_6(self, tmpdir, launcher_name, overrides):
        demo_6_sweep_test_impl(
            tmpdir, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_sweep_1_job(self, sweep_runner, launcher_name, overrides):  # noqa: F811
        demos_sweep_1_job_test_impl(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_sweep_2_jobs(self, sweep_runner, launcher_name, overrides):  # noqa: F811
        demos_sweep_2_jobs_test_impl(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_not_sweeping_hydra_overrides(
        self, sweep_runner, launcher_name, overrides
    ):  # noqa: F811
        not_sweeping_hydra_overrides(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_sweep_1_job_strict(
        self, sweep_runner, launcher_name, overrides
    ):  # noqa: F811
        demos_sweep_1_job_test_impl(
            sweep_runner,
            strict=True,
            overrides=["hydra/launcher=" + launcher_name] + overrides,
        )

    def test_sweep_1_job_strict_and_bad_key(
        self, sweep_runner, launcher_name, overrides
    ):  # noqa: F811
        with pytest.raises(KeyError):
            demos_sweep_1_job_test_impl(
                sweep_runner,
                strict=True,
                overrides=["hydra/launcher=" + launcher_name, "foo=bar"] + overrides,
            )

    def test_sweep_2_optimizers(self, sweep_runner, launcher_name, overrides):
        sweep_over_two_optimizers(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )


def demo_6_sweep_test_impl(tmpdir, overrides):
    """
    Runs a sweep with the config from demo 6
    """
    cmd = [sys.executable, "demos/6_sweep/experiment.py"]
    cmd.extend(["--multirun", "hydra.sweep.dir={}".format(str(tmpdir))])
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
