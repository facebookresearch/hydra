# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Common test functions testing launchers
"""

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import verify_dir_outputs


class LauncherTestSuite:
    def test_sweep_1_job(self, sweep_runner, launcher_name, overrides):  # noqa: F811
        sweep_1_job(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_sweep_2_jobs(self, sweep_runner, launcher_name, overrides):  # noqa: F811
        sweep_2_jobs(
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
        sweep_1_job(
            sweep_runner,
            strict=True,
            overrides=["hydra/launcher=" + launcher_name] + overrides,
        )

    def test_sweep_1_job_strict_and_bad_key(
        self, sweep_runner, launcher_name, overrides
    ):  # noqa: F811
        with pytest.raises(KeyError):
            sweep_1_job(
                sweep_runner,
                strict=True,
                overrides=["hydra/launcher=" + launcher_name, "boo=bar"] + overrides,
            )

    def test_sweep_2_optimizers(self, sweep_runner, launcher_name, overrides):
        sweep_two_config_groups(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )


def sweep_1_job(sweep_runner, overrides, strict=False):
    """
    Runs a sweep with one job
    """
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        overrides=overrides,
        strict=strict,
    )
    with sweep:
        job_ret = sweep.returns[0]
        assert len(job_ret) == 1
        assert job_ret[0].overrides == []
        assert job_ret[0].cfg == {"foo": 10, "bar": 100}
        assert job_ret[0].hydra_cfg.hydra.job.name == "a_module"
        verify_dir_outputs(sweep.returns[0][0])


def sweep_2_jobs(sweep_runner, overrides):
    """
    Runs a sweep with two jobs
    """
    overrides.append("a=0,1")
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        overrides=overrides,
    )
    base = OmegaConf.create({"foo": 10, "bar": 100, "a": 0})

    with sweep:
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            expected_conf = OmegaConf.merge(
                base, OmegaConf.from_dotlist(job_ret.overrides)
            )
            assert job_ret.overrides == ["a={}".format(i)]
            assert job_ret.cfg == expected_conf
            assert job_ret.hydra_cfg.hydra.job.name == "a_module"
            verify_dir_outputs(job_ret, job_ret.overrides)


def not_sweeping_hydra_overrides(sweep_runner, overrides):
    """
    Runs a sweep with two jobs
    """
    overrides.extend(["a=0,1", "hydra.foo=1,2,3"])
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        overrides=overrides,
    )
    base = OmegaConf.create({"foo": 10, "bar": 100})

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


def sweep_two_config_groups(sweep_runner, overrides):
    """
    Make sure that optimizers=adam,nesterov is interpreted correctly
    """
    overrides.extend(["group1=file1,file2"])
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        overrides=overrides,
    )
    expected_overrides = [["group1=file1"], ["group1=file2"]]
    expected_conf = [
        OmegaConf.create({"foo": 10, "bar": 100}),
        OmegaConf.create({"foo": 20, "bar": 100}),
    ]
    with sweep:
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            assert job_ret.overrides == expected_overrides[i]
            assert job_ret.cfg == expected_conf[i]
            verify_dir_outputs(job_ret, job_ret.overrides)
